#!/usr/bin/python3

#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#


import os
import sys
import shlex
import subprocess
import gettext


import config


from ovirt_engine import configfile
from ovirt_engine import service
from ovirt_engine import util
from ovirt_engine import java


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


class Daemon(service.Daemon):

    def __init__(self):
        super(Daemon, self).__init__()
        self._tempDir = None
        self._defaults = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.argv[0]),
                'ovirt-engine-dwhd.conf',
            )
        )

    def _getClasspath(self):
        p = subprocess.Popen(
            args=(
                os.path.join(
                    self._config.get('PKG_DATA_DIR'),
                    'bin',
                    'dwh-classpath.sh',
                ),
                'run',
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        stdout, stderr = p.communicate()
        stdout = stdout.decode('utf-8', 'replace').splitlines()
        stderr = stderr.decode('utf-8', 'replace').splitlines()
        if p.returncode != 0:
            raise RuntimeError(_('Cannot setup classpath (%s)') % stderr)
        classpath = stdout[0]
        self.logger.debug('classpath: %s', classpath)
        return classpath

    def _checkInstallation(
        self,
        pidfile,
    ):
        # Check the required directories and files:
        self.check(
            os.path.join(
                self._config.get('PKG_DATA_DIR'),
                'services',
            ),
            directory=True,
        )
        self.check(
            self._config.get('PKG_LOG_DIR'),
            directory=True,
            writable=True,
        )
        self.check(
            os.path.join(
                self._config.get('PKG_JAVA_LIB'),
                'historyETL.jar',
            ),
        )
        for log in ('ovirt-engine-dwhd.log',):
            self.check(
                name=os.path.join(
                    self._config.get('PKG_LOG_DIR'),
                    log,
                ),
                mustExist=False,
                writable=True,
            )
        if pidfile is not None:
            self.check(
                name=pidfile,
                writable=True,
                mustExist=False,
            )

    def _executeEngineDbQuery(self, query, params, operation_description):
        """
        Execute a query on the engine database.
        
        Args:
            query: SQL query string
            params: Tuple of parameters for the query
            operation_description: Description of the operation for logging
            
        Returns:
            True on success, False on failure
        """
        try:
            import psycopg2
            
            conn = psycopg2.connect(
                host=self._config.get('ENGINE_DB_HOST'),
                port=self._config.get('ENGINE_DB_PORT'),
                database=self._config.get('ENGINE_DB_DATABASE'),
                user=self._config.get('ENGINE_DB_USER'),
                password=self._config.get('ENGINE_DB_PASSWORD'),
                connect_timeout=10
            )
            
            try:
                cur = conn.cursor()
                cur.execute(query, params)
                conn.commit()
                cur.close()
                
                self.logger.debug('Successfully %s', operation_description)
                return True
            finally:
                conn.close()
                
        except ImportError:
            self.logger.warning(
                'psycopg2 module not available, cannot %s', operation_description
            )
            return False
        except Exception as e:
            self.logger.warning(
                'Exception while %s: %s', operation_description, e
            )
            return False

    def externalProcessGracefulShutdown(self, process):
        self.logger.info('Setting DisconnectDwh flag to request graceful shutdown')
        return self._executeEngineDbQuery(
            "UPDATE vdc_options SET option_value = %s WHERE option_name = %s",
            ('1', 'DisconnectDwh'),
            'set DisconnectDwh flag to 1'
        )

    def daemonSetup(self):

        if os.geteuid() == 0:
            raise RuntimeError(
                _('This service cannot be executed as root')
            )

        if not os.path.exists(self._defaults):
            raise RuntimeError(
                _(
                    "The configuration defaults file '{file}' "
                    "required but missing"
                ).format(
                    file=self._defaults,
                )
            )

        self._config = configfile.ConfigFile(
            (
                self._defaults,
                config.DWH_VARS,
            ),
        )

        #
        # the earliest so we can abort early.
        #
        self._executable = os.path.join(
            java.Java().getJavaHome(),
            'bin',
            'java',
        )

        self._checkInstallation(
            pidfile=self.pidfile,
        )

        self._tempDir = service.TempDir()
        self._tempDir.create()

        settings = os.path.join(self._tempDir.directory, 'settings.properties')
        with open(settings, 'w') as f:
            f.write(
                util.processTemplate(
                    os.path.join(
                        self._config.get('PKG_DATA_DIR'),
                        'conf',
                        'settings.properties.in'
                    ),
                    dict(
                        ('@%s@' % k, util.escape(v, ':=\\ ')) for (k, v) in
                        self._config.values.items()
                    ),
                )
            )

        self._serviceArgs = [
            'ovirt-engine-dwhd',
            '-Dorg.ovirt.engine.dwh.settings=%s' % settings,
        ]

        # Add arguments for the java heap size:
        self._serviceArgs.extend([
            '-Xms%s' % self._config.get('DWH_HEAP_MIN'),
            '-Xmx%s' % self._config.get('DWH_HEAP_MAX'),
        ])

        for engineProperty in shlex.split(
            self._config.get('DWH_PROPERTIES')
        ):
            if not engineProperty.startswith('-D'):
                engineProperty = '-D' + engineProperty
            self._serviceArgs.append(engineProperty)

        for arg in shlex.split(self._config.get('DWH_JVM_ARGS')):
            self._serviceArgs.append(arg)

        engineDebugAddress = self._config.get('DWH_DEBUG_ADDRESS')
        if engineDebugAddress:
            self._serviceArgs.append(
                (
                    '-Xrunjdwp:transport=dt_socket,address=%s,'
                    'server=y,suspend=n'
                ) % (
                    engineDebugAddress
                )
            )

        if self._config.getboolean('DWH_VERBOSE_GC'):
            self._serviceArgs.extend([
                '-verbose:gc',
                '-XX:+PrintGCTimeStamps',
                '-XX:+PrintGCDetails',
            ])

        self._serviceArgs.extend([
            '-classpath', '%s:%s' % (
                os.path.join(
                    self._config.get('PKG_JAVA_LIB'),
                    '*',
                ),
                self._getClasspath(),
            ),
            'ovirt_engine_dwh.historyetl_4_5.HistoryETL',
            '--context=Default',
        ])

        self._serviceEnv = os.environ.copy()
        self._serviceEnv.update({
            'PATH': (
                '/usr/local/sbin:/usr/local/bin:'
                '/usr/sbin:/usr/bin:/sbin:/bin'
            ),
            'LANG': 'en_US.UTF-8',
            'LC_ALL': 'en_US.UTF-8',
        })

    def daemonStdHandles(self):
        consoleLog = open(
            os.path.join(
                self._config.get('PKG_LOG_DIR'),
                'ovirt-engine-dwhd.log'
            ),
            'a+',
        )
        return (consoleLog, consoleLog)

    def daemonContext(self):
        self.logger.info('Resetting DisconnectDwh flag to 0')
        self._executeEngineDbQuery(
            "UPDATE vdc_options SET option_value = %s WHERE option_name = %s",
            ('0', 'DisconnectDwh'),
            'reset DisconnectDwh flag to 0'
        )

        self.daemonAsExternalProcess(
            executable=self._executable,
            args=self._serviceArgs,
            env=self._serviceEnv,
            stopTime=self._config.getinteger(
                'DAEMON_STOP_TIME'
            ),
            stopInterval=self._config.getinteger(
                'DAEMON_STOP_INTERVAL'
            ),
        )

    def daemonCleanup(self):
        if self._tempDir:
            self._tempDir.destroy()


if __name__ == '__main__':
    service.setupLogger()
    d = Daemon()
    d.run()


# vim: expandtab tabstop=4 shiftwidth=4
