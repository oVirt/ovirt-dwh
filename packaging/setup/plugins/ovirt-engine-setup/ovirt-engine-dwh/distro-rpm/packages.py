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


"""
Package upgrade plugin.
"""

import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-dwh')


from otopi import util
from otopi import plugin


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import dwhconstants as odwhcons


@util.export
class Plugin(plugin.PluginBase):
    """
    Package upgrade plugin.
    """

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.RPMDistroEnv.PACKAGES,
            odwhcons.Const.OVIRT_ENGINE_DWH_PACKAGE_NAME
        )
        self.environment.setdefault(
            odwhcons.RPMDistroEnv.PACKAGES_SETUP,
            odwhcons.Const.OVIRT_ENGINE_DWH_SETUP_PACKAGE_NAME
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        after=(
            odwhcons.Stages.CORE_ENABLE,
        ),
        before=(
            osetupcons.Stages.DISTRO_RPM_PACKAGE_UPDATE_CHECK,
        )
    )
    def _customization(self):
        def tolist(s):
            return [e.strip() for e in s.split(',')]

        self.environment[
            osetupcons.RPMDistroEnv.PACKAGES_SETUP
        ].extend(
            tolist(self.environment[odwhcons.RPMDistroEnv.PACKAGES_SETUP])
        )

        if self.environment[odwhcons.CoreEnv.ENABLE]:
            self.environment[
                osetupcons.RPMDistroEnv.PACKAGES_UPGRADE_LIST
            ].append(
                {
                    'packages': tolist(
                        self.environment[
                            odwhcons.RPMDistroEnv.PACKAGES
                        ]
                    ),
                },
            )


# vim: expandtab tabstop=4 shiftwidth=4
