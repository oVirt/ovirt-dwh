#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#


"""Grafana FQDN plugin."""


import gettext

from otopi import plugin
from otopi import util

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_engine_setup.engine_common import constants as oengcommcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Grafana FQDN plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: self.environment[ogdwhcons.CoreEnv.ENABLE],
        after=(
            osetupcons.Stages.CONFIG_PROTOCOLS_CUSTOMIZATION,
        ),
        before=(
            oengcommcons.Stages.NETWORK_OWNERS_CONFIG_CUSTOMIZED,
        ),
    )
    def _customization(self):
        self.environment[
            ogdwhcons.ConfigEnv.GRAFANA_FQDN
        ] = self.environment[
            osetupcons.ConfigEnv.FQDN
        ]


# vim: expandtab tabstop=4 shiftwidth=4
