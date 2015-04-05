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
from otopi import transaction
from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


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
            if not self._parent.environment[odwhcons.EngineCoreEnv.ENABLE]:
                engine_conn = self._parent.environment[
                    odwhcons.EngineDBEnv.CONNECTION
                ]
                if engine_conn is not None:
                    engine_conn.rollback()
                    self._parent.environment[
                        odwhcons.EngineDBEnv.CONNECTION
                    ] = None

        def commit(self):
            if not self._parent.environment[odwhcons.EngineCoreEnv.ENABLE]:
                engine_conn = self._parent.environment[
                    odwhcons.EngineDBEnv.CONNECTION
                ]
                if engine_conn is not None:
                    engine_conn.commit()

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            self.DBTransaction(self)
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
            oengcommcons.Stages.DB_OWNERS_CONNECTIONS_CUSTOMIZED,
        ),
    )
    def _engine_customization(self):
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.ENGINE_DB_ENV_KEYS,
        )
        dbovirtutils.getCredentials(
            name='Engine',
            queryprefix='OVESETUP_ENGINE_DB_',
            defaultdbenvkeys={
                'host': '',
                'port': '5432',
                'secured': '',
                'hostValidation': False,
                'user': 'engine',
                'password': None,
                'database': 'engine',
            },
            show_create_msg=False,
            credsfile=(
                odwhcons.FileLocations.
                OVIRT_ENGINE_ENGINE_SERVICE_CONFIG_DATABASE
            ),
        )


# vim: expandtab tabstop=4 shiftwidth=4
