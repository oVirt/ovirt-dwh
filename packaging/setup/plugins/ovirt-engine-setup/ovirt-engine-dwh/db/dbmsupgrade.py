#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2017 Red Hat, Inc.
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


"""Local Postgres upgrade plugin."""

import gettext

from otopi import plugin
from otopi import transaction
from otopi import util

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common import postgres
from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Local Postgres upgrade plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._upgrade_approved = False
        self._upgrade_approved_inplace = False
        self._upgrade_approved_cleanupold = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: (
            self.environment[
                odwhcons.CoreEnv.ENABLE
            ] and self.environment[
                odwhcons.DBEnv.NEED_DBMSUPGRADE
            ]
        ),
        name=oengcommcons.Stages.DB_CUST_UPGRADEDBMS_DWH,
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            oengcommcons.Stages.DB_CUST_UPGRADEDBMS_ENGINE,
            oengcommcons.Stages.DB_CONNECTION_CUSTOMIZATION,
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
        ),
    )
    def _customization(self):
        if self.environment[oenginecons.EngineDBEnv.NEED_DBMSUPGRADE]:
            if (
                self.environment[
                    odwhcons.DBEnv.HOST
                ] == self.environment[
                    oenginecons.EngineDBEnv.HOST
                ] and self.environment[
                    odwhcons.DBEnv.PORT
                ] == self.environment[
                    oenginecons.EngineDBEnv.PORT
                ]
            ):
                self.logger.info(_(
                    'Engine DB and DWH one shares the same PostgreSQL '
                    'instance that is going to be upgraded'
                ))
                return
            else:
                self.logger.info(_(
                    'Engine DB and DWH one are on two distinct PostgreSQL '
                    'instances and both of them have to be upgraded.'
                ))
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        )
        (
            self._upgrade_approved,
            self._upgrade_approved_inplace,
            self._upgrade_approved_cleanupold
        ) = dbovirtutils.DBMSUpgradeCustomizationHelper('DWH')

    @plugin.event(
        stage=plugin.Stages.STAGE_EARLY_MISC,
        condition=lambda self: self._upgrade_approved,
        name=oengcommcons.Stages.DB_UPGRADEDBMS_DWH,
    )
    def _updateDBMS(self):
        self.logger.info(_('Upgrading PostgreSQL'))
        with transaction.Transaction() as localtransaction:
            localtransaction.append(
                postgres.DBMSUpgradeTransaction(
                    parent=self,
                    inplace=self._upgrade_approved_inplace,
                    cleanupold=self._upgrade_approved_cleanupold,
                    upgrade_from=self.environment[
                        oengcommcons.ProvisioningEnv.OLD_POSTGRES_SERVICE
                    ],
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
