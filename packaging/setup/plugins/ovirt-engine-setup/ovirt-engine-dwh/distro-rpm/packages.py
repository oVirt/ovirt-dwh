#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""
Package upgrade plugin.
"""

import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


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
            packages = tolist(
                self.environment[
                    odwhcons.RPMDistroEnv.PACKAGES
                ]
            )
            self.environment[
                osetupcons.RPMDistroEnv.PACKAGES_UPGRADE_LIST
            ].append(
                {
                    'packages': packages,
                },
            )
            self.environment[
                osetupcons.RPMDistroEnv.VERSION_LOCK_APPLY
            ].extend(packages)

            self.environment[
                osetupcons.RPMDistroEnv.VERSION_LOCK_FILTER
            ].extend(
                tolist(
                    self.environment[odwhcons.RPMDistroEnv.PACKAGES]
                )
            )
            self.environment[
                osetupcons.RPMDistroEnv.VERSION_LOCK_FILTER
            ].extend(
                tolist(
                    self.environment[odwhcons.RPMDistroEnv.PACKAGES_SETUP]
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
