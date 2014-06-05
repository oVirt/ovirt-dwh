#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013 Red Hat, Inc.
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


"""Local Postgres plugin."""


import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-dwh')


from otopi import util
from otopi import plugin


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup import dialog
from ovirt_engine_setup.engine_common import postgres
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


@util.export
class Plugin(plugin.PluginBase):
    """Local Postgres plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = False
        self._renamedDBResources = False
        self._provisioning = postgres.Provisioning(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            defaults=odwhcons.Const.DEFAULT_DWH_DB_ENV_KEYS,
        )

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

        self._enabled = self._provisioning.supported()

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            odwhcons.Stages.DB_CONNECTION_CUSTOMIZATION,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
        ),
        condition=lambda self: self._enabled,
    )
    def _customization(self):
        enabled = self.environment[
            odwhcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED
        ]

        if not self.environment[odwhcons.CoreEnv.ENABLE]:
            enabled = False

        if enabled is None:
            local = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_DWH_PROVISIONING_POSTGRES_LOCATION',
                note=_(
                    'Where is the DWH database located? '
                    '(@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                true=_('Local'),
                false=_('Remote'),
                default=True,
            )
            if local:
                self.environment[odwhcons.DBEnv.HOST] = 'localhost'
                self.environment[
                    odwhcons.DBEnv.PORT
                ] = odwhcons.Defaults.DEFAULT_DB_PORT

                enabled = dialog.queryBoolean(
                    dialog=self.dialog,
                    name='OVESETUP_DWH_PROVISIONING_POSTGRES_ENABLED',
                    note=_(
                        'Setup can configure the local postgresql server '
                        'automatically for the DWH to run. This may '
                        'conflict with existing applications.\n'
                        'Would you like Setup to automatically configure '
                        'postgresql and create DWH database, '
                        'or prefer to perform that '
                        'manually? (@VALUES@) [@DEFAULT@]: '
                    ),
                    prompt=True,
                    true=_('Automatic'),
                    false=_('Manual'),
                    default=True,
                )

        if enabled:
            self._provisioning.applyEnvironment()

        self.environment[
            odwhcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED
        ] = self._enabled = enabled

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        priority=plugin.Stages.PRIORITY_LAST,
        condition=lambda self: self.environment[
            odwhcons.DBEnv.HOST
        ] == 'localhost',
    )
    def _customization_firewall(self):
        self.environment[osetupcons.NetEnv.FIREWALLD_SERVICES].extend([
            {
                'name': 'ovirt-postgres',
                'directory': 'ovirt-common'
            },
        ])

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        condition=lambda self: self._enabled,
    )
    def _validation(self):
        self._provisioning.validate()

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        before=(
            odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
            odwhcons.Stages.DB_SCHEMA,
        ),
        after=(
            osetupcons.Stages.SYSTEM_SYSCTL_CONFIG_AVAILABLE,
        ),
        condition=lambda self: self._enabled,
    )
    def _misc(self):
        self._provisioning.provision()

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_SUMMARY,
        ),
        condition=lambda self: self._provisioning.databaseRenamed,
    )
    def _closeup(self):
        self.dialog.note(
            text=_(
                'DWH database resources:\n'
                '    Database name:      {database}\n'
                '    Database user name: {user}\n'
            ).format(
                database=self.environment[
                    odwhcons.DBEnv.DATABASE
                ],
                user=self.environment[
                    odwhcons.DBEnv.USER
                ],
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
