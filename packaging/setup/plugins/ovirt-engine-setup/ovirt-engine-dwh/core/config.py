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


"""Database plugin."""


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import filetransaction
from otopi import plugin


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
                        dbenvkeys=odwhcons.Const.ENGINE_DB_ENV_KEYS
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
