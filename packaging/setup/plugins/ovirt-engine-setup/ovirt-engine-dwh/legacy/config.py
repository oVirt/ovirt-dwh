#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import os
import re
import datetime
import configparser
import io
import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import filetransaction
from otopi import plugin


from ovirt_engine import configfile


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    _RE_LEGACY_JDBC_URL = re.compile(
        flags=re.VERBOSE,
        pattern=r"""
            jdbc\\:
            postgresql\\:
            //
            (?P<host>[^:/]+)
            (\\:(?P<port>\d+))?
            /
            (?P<database>\w+)
            (\?(?P<extra>.*))?
        """,
    )

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    def _parse_legacy_conf(self, filename):
        config = configparser.ConfigParser()
        config.optionxform = str
        with open(filename) as f:
            config.readfp(io.StringIO(u'[default]' + f.read()))
        return dict(config.items('default'))

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        condition=lambda self: os.path.exists(
            odwhcons.FileLocations.LEGACY_CONFIG
        ),
    )
    def _setup(self):
        legacy = self._parse_legacy_conf(odwhcons.FileLocations.LEGACY_CONFIG)
        current = configfile.ConfigFile(
            files=[
                odwhcons.FileLocations.
                OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DEFAULTS,
                odwhcons.FileLocations.
                OVIRT_ENGINE_DWHD_SERVICE_CONFIG,
            ],
        )

        #
        # legacy package installed file with some defaults
        # we need to ignore it if no password
        #
        if (
            not current.get('ENGINE_DB_PASSWORD') and
            legacy.get('ovirtEngineHistoryDbPassword')
        ):
            fixups = []
            for old, new in (
                ('runDeleteTime', 'DWH_DELETE_JOB_HOUR'),
                ('runInterleave', 'DWH_SAMPLING'),
                ('timeBetweenErrorEvents', 'DWH_ERROR_EVENT_INTERVAL'),
                ('hoursToKeepSamples', 'DWH_TABLES_KEEP_SAMPLES'),
                ('hoursToKeepHourly', 'DWH_TABLES_KEEP_HOURLY'),
                ('hoursToKeepDaily', 'DWH_TABLES_KEEP_DAILY'),
            ):
                if legacy.get(old) != current.get(new):
                    fixups.append('%s="%s"' % (new, legacy.get(old)))
            if fixups:
                uninstall_files = []
                self.environment[
                    osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
                ].addFiles(
                    group='ovirt_dwh_files',
                    fileList=uninstall_files,
                )
                self.environment[
                    otopicons.CoreEnv.MAIN_TRANSACTION
                ].append(
                    filetransaction.FileTransaction(
                        name=(
                            odwhcons.FileLocations.
                            OVIRT_ENGINE_DWHD_SERVICE_CONFIG_LEGACY
                        ),
                        content=fixups,
                        modifiedList=uninstall_files,
                    )
                )

            jdbcurl = self._RE_LEGACY_JDBC_URL.match(
                legacy.get('ovirtEngineHistoryDbJdbcConnection')
            )
            if (
                jdbcurl is None or
                jdbcurl.group('host') is None or
                jdbcurl.group('database') is None
            ):
                raise RuntimeError(_('Invalid legacy DWH database config'))

            self.environment[
                odwhcons.DBEnv.HOST
            ] = jdbcurl.group('host')
            self.environment[
                odwhcons.DBEnv.PORT
            ] = (
                jdbcurl.group('port') if jdbcurl.group('port') is not None
                else odwhcons.Defaults.DEFAULT_DB_PORT
            )
            self.environment[
                odwhcons.DBEnv.DATABASE
            ] = jdbcurl.group('database')
            self.environment[
                odwhcons.DBEnv.SECURED
            ] = jdbcurl.group('extra').find('ssl=true') != -1
            self.environment[
                odwhcons.DBEnv.SECURED_HOST_VALIDATION
            ] = not jdbcurl.group('extra').find(
                'sslfactory=org.postgresql.ssl.NonValidatingFactory'
            ) == -1
            self.environment[
                odwhcons.DBEnv.USER
            ] = legacy.get('ovirtEngineHistoryDbUser')
            self.environment[
                odwhcons.DBEnv.PASSWORD
            ] = legacy.get('ovirtEngineHistoryDbPassword')

            database.OvirtUtils(
                plugin=self,
                dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            ).tryDatabaseConnect()

            self.environment[odwhcons.DBEnv.NEW_DATABASE] = False
            self.environment[odwhcons.CoreEnv.ENABLE] = True

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: os.path.exists(
            odwhcons.FileLocations.LEGACY_CONFIG
        ),
    )
    def _closeup(self):
        os.rename(
            odwhcons.FileLocations.LEGACY_CONFIG,
            '%s.%s' % (
                odwhcons.FileLocations.LEGACY_CONFIG,
                datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            ),
        )


# vim: expandtab tabstop=4 shiftwidth=4
