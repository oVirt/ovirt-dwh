#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2014-2015 Red Hat, Inc.
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


import gettext


from otopi import util
from otopi import plugin
from otopi import constants as otopicons
from otopi import filetransaction


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import dialog
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import dwh_history_timekeeping as \
    engine_db_timekeeping
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._statement = None

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.DBEnv.DISCONNECT_EXISTING_DWH,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            not self.environment[odwhcons.EngineDBEnv.NEW_DATABASE]
        ),
    )
    def _validation(self):
        self._statement = database.Statement(
            dbenvkeys=odwhcons.Const.ENGINE_DB_ENV_KEYS,
            environment=self.environment,
        )
        self._db_dwh_hostname = engine_db_timekeeping.getValueFromTimekeeping(
            statement=self._statement,
            name=engine_db_timekeeping.DB_KEY_HOSTNAME
        )
        db_dwh_uuid = engine_db_timekeeping.getValueFromTimekeeping(
            statement=self._statement,
            name=engine_db_timekeeping.DB_KEY_UUID
        )

        if (
            db_dwh_uuid and
            db_dwh_uuid != self.environment[odwhcons.CoreEnv.UUID]
        ):
            if self.environment[
                odwhcons.DBEnv.DISCONNECT_EXISTING_DWH
            ] is None:
                self.environment[
                    odwhcons.DBEnv.DISCONNECT_EXISTING_DWH
                ] = dialog.queryBoolean(
                    dialog=self.dialog,
                    name='OVESETUP_DWH_DISCONNECT_EXISTING',
                    note=_(
                        'An existing DWH is configured to work with this '
                        'engine.\n'
                        'Its hostname is {hostname}.\n'
                        'A positive answer to the following question will '
                        'cause the existing DWH to be permanently '
                        'disconnected from the engine.\n'
                        'A negative answer will stop Setup.\n'
                        'Do you want to permanently disconnect this DWH from '
                        'the engine? '
                        '(@VALUES@) [@DEFAULT@]: '
                    ).format(
                        hostname=self._db_dwh_hostname,
                    ),
                    prompt=True,
                    true=_('Yes'),
                    false=_('No'),
                    default=False,
                )
            if not self.environment[
                odwhcons.DBEnv.DISCONNECT_EXISTING_DWH
            ]:
                raise RuntimeError(
                    _('An existing DWH found - Setup cancelled by user')
                )

    @plugin.event(
        stage=plugin.Stages.STAGE_TRANSACTION_BEGIN,
        after=(
            osetupcons.Stages.SYSTEM_HOSTILE_SERVICES_DETECTION,
        ),
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            not self.environment[odwhcons.EngineDBEnv.NEW_DATABASE]
        ),
    )
    def _transactionBegin(self):
        if engine_db_timekeeping.getValueFromTimekeeping(
            statement=self._statement,
            name=engine_db_timekeeping.DB_KEY_RUNNING
        ) == '1':
            self.logger.error(
                _(
                    'dwhd is currently running.\n'
                    'Its hostname is {hostname}.\n'
                    'Please stop it before running Setup.'
                ).format(
                    hostname=self._db_dwh_hostname,
                )
            )
            raise RuntimeError(_('dwhd is currently running'))

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
        after=(
            odwhcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        ),
    )
    def _misc(self):
        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_dwh_files',
            fileList=uninstall_files,
        )
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    odwhcons.FileLocations.
                    OVIRT_ENGINE_DWHD_SERVICE_CONFIG_UUID
                ),
                content='DWH_UUID={uuid}\n'.format(
                    uuid=self.environment[odwhcons.CoreEnv.UUID],
                ),
                modifiedList=uninstall_files,
            )
        )

        engine_db_timekeeping.updateValueInTimekeeping(
            statement=self.environment[odwhcons.EngineDBEnv.STATEMENT],
            name=engine_db_timekeeping.DB_KEY_HOSTNAME,
            value=self.environment[osetupcons.ConfigEnv.FQDN]
        )
        engine_db_timekeeping.updateValueInTimekeeping(
            statement=self.environment[odwhcons.EngineDBEnv.STATEMENT],
            name=engine_db_timekeeping.DB_KEY_UUID,
            value=self.environment[odwhcons.CoreEnv.UUID]
        )


# vim: expandtab tabstop=4 shiftwidth=4
