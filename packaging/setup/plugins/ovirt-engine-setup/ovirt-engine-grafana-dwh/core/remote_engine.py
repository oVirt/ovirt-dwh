#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


from ovirt_setup_lib import hostname as osetuphostname


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            oenginecons.ConfigEnv.ENGINE_FQDN,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_NETWORK,
            oengcommcons.Stages.NETWORK_OWNERS_CONFIG_CUSTOMIZED,
        ),
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_NETWORK,
        ),
        condition=lambda self: self.environment[
            ogdwhcons.CoreEnv.ENABLE
        ] and not self.environment[
            oenginecons.CoreEnv.ENABLE
        ] and not self.environment.get(
            odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED
        ),
    )
    def _remote_engine_customization(self):
        osetuphostname.Hostname(
            plugin=self,
        ).getHostname(
            envkey=oenginecons.ConfigEnv.ENGINE_FQDN,
            whichhost=_('the engine'),
            supply_default=False,
        )
        self.environment[
            osetupcons.CoreEnv.REMOTE_ENGINE
        ].configure(
            fqdn=self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
            ],
        )


# vim: expandtab tabstop=4 shiftwidth=4
