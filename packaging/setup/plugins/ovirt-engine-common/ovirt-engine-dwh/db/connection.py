#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Connection plugin."""


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import plugin


from ovirt_engine import configfile


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Connection plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_BOOT,
    )
    def _boot(self):
        self.environment[
            otopicons.CoreEnv.LOG_FILTER_KEYS
        ].append(
            odwhcons.DBEnv.PASSWORD
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.DBEnv.HOST,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.PORT,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.SECURED,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.SECURED_HOST_VALIDATION,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.USER,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.PASSWORD,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.DATABASE,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.DUMPER,
            odwhcons.Defaults.DEFAULT_DB_DUMPER
        )
        self.environment.setdefault(
            odwhcons.DBEnv.FILTER,
            odwhcons.Defaults.DEFAULT_DB_FILTER
        )
        self.environment.setdefault(
            odwhcons.DBEnv.RESTORE_JOBS,
            odwhcons.Defaults.DEFAULT_DB_RESTORE_JOBS
        )

        # TODO: probably we can add helper function within database.py to get
        # dbkeys and set all to none, instead of duplicating this.

        self.environment[odwhcons.DBEnv.CONNECTION] = None
        self.environment[odwhcons.DBEnv.STATEMENT] = None
        self.environment[odwhcons.DBEnv.NEW_DATABASE] = True
        self.environment[odwhcons.DBEnv.NEED_DBMSUPGRADE] = False

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _commands(self):
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        )
        dbovirtutils.detectCommands()

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        name=odwhcons.Stages.DB_CONNECTION_SETUP,
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and (
                self.environment[
                    osetupcons.CoreEnv.ACTION
                ] != osetupcons.Const.ACTION_PROVISIONDB
            )
        ),
    )
    def _setup(self):
        config = configfile.ConfigFile([
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DEFAULTS,
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG,
        ])
        if config.get('DWH_DB_PASSWORD'):
            try:
                dbenv = {}
                for e, k in (
                    (odwhcons.DBEnv.HOST, 'DWH_DB_HOST'),
                    (odwhcons.DBEnv.PORT, 'DWH_DB_PORT'),
                    (odwhcons.DBEnv.USER, 'DWH_DB_USER'),
                    (odwhcons.DBEnv.PASSWORD, 'DWH_DB_PASSWORD'),
                    (odwhcons.DBEnv.DATABASE, 'DWH_DB_DATABASE'),
                ):
                    dbenv[e] = (
                        self.environment.get(e)
                        if self.environment.get(e) is not None
                        else config.get(k)
                    )
                for e, k in (
                    (odwhcons.DBEnv.SECURED, 'DWH_DB_SECURED'),
                    (
                        odwhcons.DBEnv.SECURED_HOST_VALIDATION,
                        'DWH_DB_SECURED_VALIDATION'
                    )
                ):
                    dbenv[e] = config.getboolean(k)

                dbovirtutils = database.OvirtUtils(
                    plugin=self,
                    dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
                )
                dbovirtutils.tryDatabaseConnect(dbenv)
                self.environment.update(dbenv)
                self.environment[
                    odwhcons.DBEnv.NEW_DATABASE
                ] = dbovirtutils.isNewDatabase()
                self.environment[
                    odwhcons.DBEnv.NEED_DBMSUPGRADE
                ] = dbovirtutils.checkDBMSUpgrade()
            except RuntimeError:
                self.logger.debug(
                    'Existing credential use failed',
                    exc_info=True,
                )
                msg = _(
                    'Cannot connect to DWH database using existing '
                    'credentials: {user}@{host}:{port}'
                ).format(
                    host=dbenv[odwhcons.DBEnv.HOST],
                    port=dbenv[odwhcons.DBEnv.PORT],
                    database=dbenv[odwhcons.DBEnv.DATABASE],
                    user=dbenv[odwhcons.DBEnv.USER],
                )
                if self.environment[
                    osetupcons.CoreEnv.ACTION
                ] == osetupcons.Const.ACTION_REMOVE:
                    self.logger.warning(msg)
                else:
                    raise RuntimeError(msg)


# vim: expandtab tabstop=4 shiftwidth=4
