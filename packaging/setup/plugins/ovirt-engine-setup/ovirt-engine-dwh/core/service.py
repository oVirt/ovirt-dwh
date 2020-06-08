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
from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: (
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ] and
            self.environment[
                odwhcons.CoreEnv.ENABLE
            ]
        ),
    )
    def _closeup(self):
        self.logger.info(_('Starting dwh service'))
        self.services.state(
            name=odwhcons.Const.SERVICE_NAME,
            state=True,
        )
        self.services.startup(
            name=odwhcons.Const.SERVICE_NAME,
            state=True,
        )


# vim: expandtab tabstop=4 shiftwidth=4
