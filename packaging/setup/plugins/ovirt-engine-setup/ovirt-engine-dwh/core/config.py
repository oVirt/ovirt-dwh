#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Database plugin."""


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import filetransaction
from otopi import plugin


from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Databsae plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.DB_SCHEMA,
        ),
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
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
                    OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DATABASE
                ),
                mode=0o600,
                owner=self.environment[osetupcons.SystemEnv.USER_ENGINE],
                enforcePermissions=True,
                content='%s%s' % (
                    database.OvirtUtils(
                        plugin=self,
                        dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS
                    ).getDBConfig(
                        prefix="ENGINE"
                    ),
                    database.OvirtUtils(
                        plugin=self,
                        dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS
                    ).getDBConfig(
                        prefix="DWH"
                    )
                ),
                modifiedList=uninstall_files,
            )
        )
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    odwhcons.FileLocations.
                    OVIRT_ENGINE_ENGINE_SERVICE_CONFIG_DWH_DATABASE_EXAMPLE
                ),
                mode=0o600,
                owner=self.environment[osetupcons.SystemEnv.USER_ENGINE],
                enforcePermissions=True,
                content=database.OvirtUtils(
                    plugin=self,
                    dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS
                ).getDBConfig(
                    prefix="DWH",
                    # This file goes to the remote engine, so we
                    # override the host with our FQDN.
                    localhost_replacement=self.environment[
                        osetupcons.ConfigEnv.FQDN
                    ]
                ),
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
