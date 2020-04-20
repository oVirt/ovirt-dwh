#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2020 Red Hat, Inc.
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


"""grafana connection plugin."""


import gettext

from otopi import constants as otopicons
from otopi import plugin
from otopi import util


from ovirt_engine import configfile


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Grafana connection plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_BOOT,
    )
    def _boot(self):
        self.environment[
            otopicons.CoreEnv.LOG_FILTER_KEYS
        ].append(
            ogdwhcons.GrafanaDBEnv.PASSWORD
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.GrafanaDBEnv.USER,
            None
        )
        self.environment.setdefault(
            ogdwhcons.GrafanaDBEnv.PASSWORD,
            None
        )
        self.environment[ogdwhcons.GrafanaDBEnv.CONNECTION] = None
        self.environment[ogdwhcons.GrafanaDBEnv.STATEMENT] = None

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _commands(self):
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=ogdwhcons.Const.DWH_DB_ENV_KEYS,
        )
        dbovirtutils.detectCommands()

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        name=ogdwhcons.Stages.DB_CONNECTION_SETUP,
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and (
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
        if config.get('GRAFANA_DB_PASSWORD'):
            try:
                dbenv = {}
                for e, k in (
                    (odwhcons.DBEnv.HOST, 'GRAFANA_DB_HOST'),
                    (odwhcons.DBEnv.PORT, 'GRAFANA_DB_PORT'),
                    (ogdwhcons.GrafanaDBEnv.USER, 'GRAFANA_DB_USER'),
                    (ogdwhcons.GrafanaDBEnv.PASSWORD, 'GRAFANA_DB_PASSWORD'),
                    (odwhcons.DBEnv.DATABASE, 'GRAFANA_DB_DATABASE'),
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
                    dbenvkeys=ogdwhcons.Const.GRAFANA_DB_ENV_KEYS,
                )
                dbovirtutils.tryDatabaseConnect(dbenv)
                self.environment.update(dbenv)
            except RuntimeError:
                self.logger.debug(
                    'Existing credential use failed',
                    exc_info=True,
                )
                msg = _(
                    'Cannot connect to database for grafana using existing '
                    'credentials: {user}@{host}:{port}'
                ).format(
                    host=dbenv[odwhcons.DBEnv.HOST],
                    port=dbenv[odwhcons.DBEnv.PORT],
                    database=dbenv[odwhcons.DBEnv.DATABASE],
                    user=dbenv[ogdwhcons.GrafanaDBEnv.USER],
                )
                if self.environment[
                    osetupcons.CoreEnv.ACTION
                ] == osetupcons.Const.ACTION_REMOVE:
                    self.logger.warning(msg)
                else:
                    raise RuntimeError(msg)


# vim: expandtab tabstop=4 shiftwidth=4
