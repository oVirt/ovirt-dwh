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


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


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
            ogdwhcons.ConfigEnv.GRAFANA_SERVICE_STOP_NEEDED,
            True
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_TRANSACTION_BEGIN,
        before=(
            osetupcons.Stages.SYSTEM_HOSTILE_SERVICES_DETECTION,
        ),
        condition=lambda self: not self.environment[
            osetupcons.CoreEnv.DEVELOPER_MODE
        ] and self.environment[
            ogdwhcons.ConfigEnv.GRAFANA_SERVICE_STOP_NEEDED
        ],
    )
    def _transactionBegin(self):
        self.environment[
            osetupcons.SystemEnv.HOSTILE_SERVICES
        ] = '{current},{grafana}'.format(
            current=self.environment[osetupcons.SystemEnv.HOSTILE_SERVICES],
            grafana=ogdwhcons.Const.SERVICE_NAME,
        )


# vim: expandtab tabstop=4 shiftwidth=4
