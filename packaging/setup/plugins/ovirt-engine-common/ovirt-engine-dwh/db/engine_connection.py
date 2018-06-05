#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013-2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Connection plugin."""


import gettext


from otopi import constants as otopicons
from otopi import plugin
from otopi import transaction
from otopi import util


from ovirt_engine import configfile

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Connection plugin."""

    class DBTransaction(transaction.TransactionElement):
        """yum transaction element."""

        def __init__(self, parent):
            self._parent = parent

        def __str__(self):
            return _("DWH Engine database Transaction")

        def prepare(self):
            pass

        def abort(self):
            if not self._parent.environment[oenginecons.CoreEnv.ENABLE]:
                engine_conn = self._parent.environment[
                    oenginecons.EngineDBEnv.CONNECTION
                ]
                if engine_conn is not None:
                    engine_conn.rollback()
                    self._parent.environment[
                        oenginecons.EngineDBEnv.CONNECTION
                    ] = None

        def commit(self):
            if not self._parent.environment[oenginecons.CoreEnv.ENABLE]:
                engine_conn = self._parent.environment[
                    oenginecons.EngineDBEnv.CONNECTION
                ]
                if engine_conn is not None:
                    engine_conn.commit()

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_BOOT,
    )
    def _boot(self):
        self.environment[
            otopicons.CoreEnv.LOG_FILTER_KEYS
        ].append(
            oenginecons.EngineDBEnv.PASSWORD
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            oenginecons.EngineDBEnv.HOST,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.PORT,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.SECURED,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.SECURED_HOST_VALIDATION,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.USER,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.PASSWORD,
            None
        )
        self.environment.setdefault(
            oenginecons.EngineDBEnv.DATABASE,
            None
        )

        self.environment[oenginecons.EngineDBEnv.CONNECTION] = None
        self.environment[oenginecons.EngineDBEnv.STATEMENT] = None
        self.environment[oenginecons.EngineDBEnv.NEW_DATABASE] = True
        self.environment[oenginecons.EngineDBEnv.NEED_DBMSUPGRADE] = False

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup_dbtransaction(self):
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            self.DBTransaction(self)
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        after=(
            oengcommcons.Stages.DB_CONNECTION_SETUP,
        ),
        # If engine is enabled too, we let its plugin read the setup
        condition=lambda self: not self.environment[
            oenginecons.CoreEnv.ENABLE
        ] and (
            self.environment[
                osetupcons.CoreEnv.ACTION
            ] != osetupcons.Const.ACTION_PROVISIONDB
        ),
    )
    def _setup_engine_db_credentials(self):
        # TODO: refactor the code in this function to be usable by similar
        # ones
        config = configfile.ConfigFile([
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DEFAULTS,
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG,
        ])
        if config.get('ENGINE_DB_PASSWORD'):
            try:
                dbenv = {}
                for e, k in (
                    (oenginecons.EngineDBEnv.HOST, 'ENGINE_DB_HOST'),
                    (oenginecons.EngineDBEnv.PORT, 'ENGINE_DB_PORT'),
                    (oenginecons.EngineDBEnv.USER, 'ENGINE_DB_USER'),
                    (oenginecons.EngineDBEnv.PASSWORD, 'ENGINE_DB_PASSWORD'),
                    (oenginecons.EngineDBEnv.DATABASE, 'ENGINE_DB_DATABASE'),
                ):
                    dbenv[e] = (
                        self.environment.get(e)
                        if self.environment.get(e) is not None
                        else config.get(k)
                    )
                for e, k in (
                    (oenginecons.EngineDBEnv.SECURED, 'ENGINE_DB_SECURED'),
                    (
                        oenginecons.EngineDBEnv.SECURED_HOST_VALIDATION,
                        'ENGINE_DB_SECURED_VALIDATION'
                    )
                ):
                    dbenv[e] = config.getboolean(k)

                dbovirtutils = database.OvirtUtils(
                    plugin=self,
                    dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
                )
                dbovirtutils.tryDatabaseConnect(dbenv)
                self.environment.update(dbenv)
                self.environment[
                    oenginecons.EngineDBEnv.NEW_DATABASE
                ] = dbovirtutils.isNewDatabase()
                self.environment[
                    oenginecons.EngineDBEnv.NEED_DBMSUPGRADE
                ] = dbovirtutils.checkDBMSUpgrade()
            except RuntimeError as e:
                self.logger.debug(
                    'Existing credential use failed',
                    exc_info=True,
                )
                msg = _(
                    'Cannot connect to Engine database using existing '
                    'credentials: {user}@{host}:{port}'
                ).format(
                    host=dbenv[oenginecons.EngineDBEnv.HOST],
                    port=dbenv[oenginecons.EngineDBEnv.PORT],
                    database=dbenv[oenginecons.EngineDBEnv.DATABASE],
                    user=dbenv[oenginecons.EngineDBEnv.USER],
                )
                if self.environment[
                    osetupcons.CoreEnv.ACTION
                ] == osetupcons.Const.ACTION_REMOVE:
                    self.logger.warning(msg)
                else:
                    raise RuntimeError(msg)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=odwhcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            # If engine is enabled, STATEMENT and CONNECTION are set there
            not self.environment[oenginecons.CoreEnv.ENABLE]
        ),
        after=(
            odwhcons.Stages.DB_SCHEMA,
            oengcommcons.Stages.DB_CONNECTION_AVAILABLE,
        ),
    )
    def _engine_connection(self):
        self.environment[
            oenginecons.EngineDBEnv.STATEMENT
        ] = database.Statement(
            environment=self.environment,
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
        )
        # must be here as we do not have database at validation
        self.environment[
            oenginecons.EngineDBEnv.CONNECTION
        ] = self.environment[oenginecons.EngineDBEnv.STATEMENT].connect()


# vim: expandtab tabstop=4 shiftwidth=4
