#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""DWH Database plugin."""


import gettext

from otopi import constants as otopicons
from otopi import filetransaction
from otopi import plugin
from otopi import util

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common import dwh_history_timekeeping


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = False

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.CoreEnv.ENABLE,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.DB_SCHEMA,
        ),
        condition=lambda self: (
            self.environment[oenginecons.CoreEnv.ENABLE] and
            self.environment[odwhcons.CoreEnv.ENABLE]
        ),
    )
    def _miscDWHConfig(self):
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    oenginecons.FileLocations.
                    OVIRT_ENGINE_SERVICE_CONFIG_DWH_DATABASE
                ),
                mode=0o600,
                owner=self.environment[osetupcons.SystemEnv.USER_ENGINE],
                enforcePermissions=True,
                content=database.OvirtUtils(
                    plugin=self,
                    dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS
                ).getDBConfig(
                    prefix="DWH"
                ),
                modifiedList=self.environment[
                    otopicons.CoreEnv.MODIFIED_FILES
                ],
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_SUMMARY,
        ),
        condition=lambda self: (
            self.environment[oenginecons.CoreEnv.ENABLE] and
            not self.environment[odwhcons.CoreEnv.ENABLE]
        ),
    )
    def _closeupDWHConfig(self):
        self._statement = database.Statement(
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
            environment=self.environment,
        )
        self._dwh_host = dwh_history_timekeeping.getValueFromTimekeeping(
            statement=self._statement,
            name=dwh_history_timekeeping.DB_KEY_HOSTNAME
        )
        if not self._dwh_host:
            self.dialog.note(
                _(
                    'The engine requires access to the Data Warehouse '
                    'database.\nData Warehouse was not set up. Please set it '
                    'up on some other machine and configure access to it on '
                    'the engine.'
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
