#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013-2017 Red Hat, Inc.
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


"""Vacuum plugin."""

import datetime
import gettext

from otopi import plugin
from otopi import util

from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import constants as oengcommcons

from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Vacuum plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.DBEnv.DWH_VACUUM_FULL,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: (
            self.environment[
                odwhcons.CoreEnv.ENABLE
            ] and not self.environment[
                odwhcons.DBEnv.NEW_DATABASE
            ]
        ),
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            oengcommcons.Stages.DB_CONNECTION_STATUS,
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
            oengcommcons.Stages.DB_CUST_UPGRADEDBMS_DWH,
        ),
    )
    def _customization(self):
        if self.environment[
            odwhcons.DBEnv.DWH_VACUUM_FULL
        ] is not None:
            return

        self.environment[
            odwhcons.DBEnv.DWH_VACUUM_FULL
        ] = dialog.queryBoolean(
            dialog=self.dialog,
            name='DWH_VACUUM_FULL',
            # TODO try to supply some estimation on the amount
            # of space we will need to read/write/remove if possible.
            # some projects like check_postgres may supply that report
            # already. See https://github.com/bucardo/check_postgres
            note=_(
                'Perform full vacuum on the oVirt engine history'
                '\ndatabase {db}@{host}?'
                '\nThis operation may take a while'
                ' depending on this setup health and the'
                '\nconfiguration of the db vacuum process.'
                '\nSee'
                ' https://www.postgresql.org/docs/10/sql-vacuum.html'
                '\n(@VALUES@) [@DEFAULT@]: '
            ).format(
                db=self.environment[
                    odwhcons.DBEnv.DATABASE
                ],
                host=self.environment[
                    odwhcons.DBEnv.HOST
                ],
            ),
            prompt=True,
            default=False
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self.environment[
            odwhcons.DBEnv.DWH_VACUUM_FULL
        ],
        after=(
            odwhcons.Stages.DB_SCHEMA,
        ),
    )
    def _vacuum(self):
        self.logger.info(
            _("Running vacuum full on the ovirt_engine_history schema")
        )
        start = datetime.datetime.now()
        args = [
            odwhcons.FileLocations.OVIRT_DWH_VACUUM_TOOL,
            '-f',
            '-v'
        ]
        self.execute(args=args)
        self.logger.info(
            _("Running vacuum full elapsed {secs}").format(
                secs=datetime.datetime.now() - start,
            )
        )
