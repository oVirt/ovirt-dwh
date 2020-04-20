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


"""Local grafana Postgres plugin."""


import gettext

from otopi import plugin
from otopi import util
from otopi import transaction

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import postgres
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Local grafana Postgres plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._provisioning = postgres.Provisioning(
            plugin=self,
            dbenvkeys=ogdwhcons.Const.GRAFANA_DB_ENV_KEYS,
            defaults=ogdwhcons.Const.DEFAULT_GRAFANA_DB_ENV_KEYS,
        )
        self._enabled = False

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        after=(
            odwhcons.Stages.DB_CONNECTION_SETUP,
        ),
        condition=lambda self: (
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ] and
            self.environment[
                odwhcons.DBEnv.NEW_DATABASE
            ]
        ),
    )
    def _setup(self):
        self._provisioning.detectCommands()

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
            ogdwhcons.Stages.DB_GRAFANA_CONNECTION_CUSTOMIZATION,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
            odwhcons.Stages.DB_PROVISIONING_CUSTOMIZATION,
        ),
        condition=lambda self: self.environment[
            ogdwhcons.CoreEnv.ENABLE
        ],
    )
    def _customization(self):
        if self.environment[
            odwhcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED
        ]:
            self._enabled = True
        elif (
            not self.environment[odwhcons.DBEnv.NEW_DATABASE] and
            not self.environment[ogdwhcons.GrafanaDBEnv.PASSWORD] and
            self.environment[odwhcons.DBEnv.HOST] == 'localhost'
        ):
            self.dialog.note(
                _(
                    'DWH database is on localhost, user for Grafana not '
                    'configured yet.'
                )
            )
            self._enabled = dialog.queryBoolean(
                dialog=self.dialog,
                name='CREATE_GRAFANA_DB_LOCAL_USER',
                note=_(
                    'Create a local user for Grafana? '
                    '(@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                true=_('Yes'),
                false=_('No'),
                default=True,
            )
        if self._enabled:
            self._provisioning.applyEnvironment()

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        condition=lambda self: self._enabled,
    )
    def _validation(self):
        self._provisioning.validate()

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.DB_SCHEMA,
        ),
        before=(
            odwhcons.Stages.DB_CONNECTION_AVAILABLE,
            # TODO: This is not enough. We restart PG here, so have to do that
            # before starting the connection, or it will be broken. But also
            # other plugins maintain connections, to engine db and cinderlib
            # db. Need to clean this up.
        ),
        condition=lambda self: self._enabled,
    )
    def _misc(self):
        self.logger.info(_('Creating a user for Grafana'))
        self._provisioning.createUser()
        with transaction.Transaction() as localtransaction:
            self._provisioning.addPgHbaDatabaseAccess(
                transaction=localtransaction,
            )
        self._provisioning.restartPG()
        self._provisioning.grantReadOnlyAccessToUser()


# vim: expandtab tabstop=4 shiftwidth=4
