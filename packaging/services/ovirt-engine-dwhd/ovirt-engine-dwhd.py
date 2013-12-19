#!/usr/bin/python

# Copyright 2012-2013 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import shlex
import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-dwh')


import config


from ovirt_engine import configfile
from ovirt_engine import service
from ovirt_engine import java


class Daemon(service.Daemon):

    def __init__(self):
        super(Daemon, self).__init__()
        self._defaults = os.path.abspath(
            os.path.join(
                os.path.dirname(sys.argv[0]),
                'ovirt-engine-dwhd.conf',
            )
        )

    def _checkInstallation(
        self,
        pidfile,
        jbossModulesJar,
    ):
        # Check the required JBoss directories and files:
        self.check(
            name=self._config.get('JBOSS_HOME'),
            directory=True,
        )
        self.check(
            name=jbossModulesJar,
        )

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

        jbossModulesJar = os.path.join(
            self._config.get('JBOSS_HOME'),
            'jboss-modules.jar',
        )

        self._checkInstallation(
            pidfile=self.pidfile,
            jbossModulesJar=jbossModulesJar,
        )

        self._serviceArgs = [
            'ovirt-engine-dwhd',
            '-Djboss.modules.write-indexes=false',
        ]

        #
        # TODO Generate file out of configuration
        #
        self._serviceArgs.extend([
            '-Dorg.ovirt.engine.dwh.settings=%s' % os.path.join(
                config.PKG_SYSCONF_DIR,
                '..',
                'ovirt-engine',
                'ovirt-engine-dwh',
                'Default.properties',
            ),
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
            '-jar', jbossModulesJar,
            '-dependencies', 'org.ovirt.engine.dwh',
            '-class', 'ovirt_engine_dwh.historyetl_3_3.HistoryETL',
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
            'CLASSPATH': '',
            'JAVA_MODULEPATH': '%s:%s' % (
                self._config.get('DWH_JAVA_MODULEPATH'),
                os.path.join(
                    self._config.get('JBOSS_HOME'),
                    'modules',
                )
            ),
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


if __name__ == '__main__':
    service.setupLogger()
    d = Daemon()
    d.run()


# vim: expandtab tabstop=4 shiftwidth=4
