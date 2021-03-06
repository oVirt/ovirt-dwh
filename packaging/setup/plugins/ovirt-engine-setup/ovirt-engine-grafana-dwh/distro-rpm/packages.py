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
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


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
            ogdwhcons.RPMDistroEnv.PACKAGES_SETUP,
            ogdwhcons.Const.OVIRT_ENGINE_GRAFANA_DWH_SETUP_PACKAGE_NAME
        )
        self.environment.setdefault(
            ogdwhcons.RPMDistroEnv.ADDITIONAL_PACKAGES,
            ogdwhcons.Defaults.DEFAULT_ADDITIONAL_PACKAGES
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
            tolist(self.environment[ogdwhcons.RPMDistroEnv.PACKAGES_SETUP])
        )

        if self.environment[odwhcons.CoreEnv.ENABLE]:
            self.environment[
                osetupcons.RPMDistroEnv.PACKAGES_UPGRADE_LIST
            ].append(
                {
                    'packages': tolist(
                        self.environment[
                            ogdwhcons.RPMDistroEnv.ADDITIONAL_PACKAGES
                        ]
                    )
                },
            )


# vim: expandtab tabstop=4 shiftwidth=4
