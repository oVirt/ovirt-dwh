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
from otopi import util


from ovirt_engine import configfile


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

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_BOOT,
    )
    def _boot(self):
        self.environment[
            otopicons.CoreEnv.LOG_FILTER_KEYS
        ].append(
            odwhcons.EngineDBEnv.PASSWORD
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.EngineDBEnv.HOST,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.PORT,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.SECURED,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.SECURED_HOST_VALIDATION,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.USER,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.PASSWORD,
            None
        )
        self.environment.setdefault(
            odwhcons.EngineDBEnv.DATABASE,
            None
        )

        self.environment[odwhcons.EngineDBEnv.CONNECTION] = None
        self.environment[odwhcons.EngineDBEnv.STATEMENT] = None
        self.environment[odwhcons.EngineDBEnv.NEW_DATABASE] = True

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        after=(
            oengcommcons.Stages.DB_CONNECTION_SETUP,
        ),
        # If engine is enabled too, we let its plugin read the setup
        condition=lambda self: not self.environment[
            odwhcons.EngineCoreEnv.ENABLE
        ],
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
                    (odwhcons.EngineDBEnv.HOST, 'ENGINE_DB_HOST'),
                    (odwhcons.EngineDBEnv.PORT, 'ENGINE_DB_PORT'),
                    (odwhcons.EngineDBEnv.USER, 'ENGINE_DB_USER'),
                    (odwhcons.EngineDBEnv.PASSWORD, 'ENGINE_DB_PASSWORD'),
                    (odwhcons.EngineDBEnv.DATABASE, 'ENGINE_DB_DATABASE'),
                ):
                    dbenv[e] = (
                        self.environment.get(e)
                        if self.environment.get(e) is not None
                        else config.get(k)
                    )
                for e, k in (
                    (odwhcons.EngineDBEnv.SECURED, 'ENGINE_DB_SECURED'),
                    (
                        odwhcons.EngineDBEnv.SECURED_HOST_VALIDATION,
                        'ENGINE_DB_SECURED_VALIDATION'
                    )
                ):
                    dbenv[e] = config.getboolean(k)

                dbovirtutils = database.OvirtUtils(
                    plugin=self,
                    dbenvkeys=odwhcons.Const.ENGINE_DB_ENV_KEYS,
                )
                dbovirtutils.tryDatabaseConnect(dbenv)
                self.environment.update(dbenv)
                self.environment[
                    odwhcons.EngineDBEnv.NEW_DATABASE
                ] = dbovirtutils.isNewDatabase()
            except RuntimeError as e:
                self.logger.debug(
                    'Existing credential use failed',
                    exc_info=True,
                )
                msg = _(
                    'Cannot connect to Engine database using existing '
                    'credentials: {user}@{host}:{port}'
                ).format(
                    host=dbenv[odwhcons.EngineDBEnv.HOST],
                    port=dbenv[odwhcons.EngineDBEnv.PORT],
                    database=dbenv[odwhcons.EngineDBEnv.DATABASE],
                    user=dbenv[odwhcons.EngineDBEnv.USER],
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
            not self.environment[odwhcons.EngineCoreEnv.ENABLE]
        ),
        after=(
            odwhcons.Stages.DB_SCHEMA,
            oengcommcons.Stages.DB_CONNECTION_AVAILABLE,
        ),
    )
    def _engine_connection(self):
        self.environment[
            odwhcons.EngineDBEnv.STATEMENT
        ] = database.Statement(
            environment=self.environment,
            dbenvkeys=odwhcons.Const.ENGINE_DB_ENV_KEYS,
        )
        # must be here as we do not have database at validation
        self.environment[
            odwhcons.EngineDBEnv.CONNECTION
        ] = self.environment[odwhcons.EngineDBEnv.STATEMENT].connect()


# vim: expandtab tabstop=4 shiftwidth=4
