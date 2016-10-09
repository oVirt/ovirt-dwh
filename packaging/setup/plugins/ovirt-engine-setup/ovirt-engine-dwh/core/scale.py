#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2016 Red Hat, Inc.
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


"""Scale plugin."""


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import filetransaction
from otopi import plugin


from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Scale plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    _DWH_SCALES = [
        {
            'index': _('1'),
            'desc': _('Basic'),
            'conf': (
                'DWH_TABLES_KEEP_SAMPLES=24',
                'DWH_TABLES_KEEP_HOURLY=720',
                'DWH_TABLES_KEEP_DAILY=0'
            ),
        },
        {
            'index': _('2'),
            'desc': _('Full'),
            'conf': (
                'DWH_TABLES_KEEP_SAMPLES=24',
                'DWH_TABLES_KEEP_HOURLY=1440',
                'DWH_TABLES_KEEP_DAILY=43800',
            ),
        },
    ]

    _DEFAULT_DWH_SCALE_WITH_ENGINE = _('1')
    _DEFAULT_DWH_SCALE_WITHOUT_ENGINE = _('2')

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ] and self.environment[
            odwhcons.DBEnv.NEW_DATABASE
        ],
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_MISC,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_MISC,
        ),
    )
    def _customization(self):
        dialog.queryEnvKey(
            name='OVESETUP_DWH_SCALE',
            dialog=self.dialog,
            logger=self.logger,
            env=self.environment,
            key=odwhcons.ConfigEnv.SCALE,
            note=_(
                'Please choose Data Warehouse sampling scale:\n'
                '{scales}'
                '\n(@VALUES@)[@DEFAULT@]: '
            ).format(
                scales='\n'.join(
                    [
                        _(
                            '({index}) {desc}'
                        ).format(
                            index=scale['index'],
                            desc=scale['desc'],
                        )
                        for scale in self._DWH_SCALES
                    ]
                ),
            ),
            default=(
                self._DEFAULT_DWH_SCALE_WITH_ENGINE
                if self.environment[oenginecons.CoreEnv.ENABLE]
                else self._DEFAULT_DWH_SCALE_WITHOUT_ENGINE
            ),
            validValues=(
                scale['index']
                for scale in self._DWH_SCALES
            ),
            prompt=True,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ] and self.environment[
            odwhcons.DBEnv.NEW_DATABASE
        ],
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
                    OVIRT_ENGINE_DWHD_SERVICE_CONFIG_SCALE
                ),
                mode=0o600,
                owner=self.environment[osetupcons.SystemEnv.USER_ENGINE],
                enforcePermissions=True,
                content=next(
                    scale['conf']
                    for scale in self._DWH_SCALES
                    if scale[
                        'index'
                    ] == self.environment[
                        odwhcons.ConfigEnv.SCALE
                    ]
                ),
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
