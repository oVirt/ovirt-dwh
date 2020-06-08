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
            ogdwhcons.ConfigEnv.GRAFANA_PORT,
            ogdwhcons.Defaults.GRAFANA_PORT
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: (
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ] and
            self.environment[
                ogdwhcons.CoreEnv.ENABLE
            ]
        ),
    )
    def _closeup_grafana_service(self):
        self.logger.info(_('Starting Grafana service'))
        self.services.state(
            name=ogdwhcons.Const.SERVICE_NAME,
            state=True,
        )
        self.services.startup(
            name=ogdwhcons.Const.SERVICE_NAME,
            state=True,
        )


# vim: expandtab tabstop=4 shiftwidth=4
