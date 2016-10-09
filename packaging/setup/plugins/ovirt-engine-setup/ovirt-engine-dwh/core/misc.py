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


import gettext


from otopi import util
from otopi import plugin

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        name=odwhcons.Stages.CORE_ENABLE,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_PRODUCT_OPTIONS,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_PRODUCT_OPTIONS,
            oenginecons.Stages.CORE_ENABLE
        ),
    )
    def _customization(self):
        if self.environment[odwhcons.CoreEnv.ENABLE] is None:
            if self.environment[oenginecons.CoreEnv.ENABLE]:
                self.dialog.note(
                    text=_(
                        'Please note: Data Warehouse is required for the '
                        'engine. If you choose to not configure it on this '
                        'host, you have to configure it on a remote host, and '
                        'then configure the engine on this host so that it '
                        'can access the database of the remote Data '
                        'Warehouse host.'
                    )
                )
            self.environment[
                odwhcons.CoreEnv.ENABLE
            ] = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_DWH_ENABLE',
                note=_(
                    'Configure Data Warehouse on this host '
                    '(@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                default=True,
            )
        if self.environment[odwhcons.CoreEnv.ENABLE]:
            self.environment[odwhcons.ConfigEnv.DWH_SERVICE_STOP_NEEDED] = True


# vim: expandtab tabstop=4 shiftwidth=4
