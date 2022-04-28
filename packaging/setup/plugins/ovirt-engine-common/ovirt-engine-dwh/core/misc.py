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
from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_BOOT,
        before=(
            osetupcons.Stages.SECRETS_FILTERED_FROM_SETUP_ATTRS_MODULES,
        ),
    )
    def _boot(self):
        self.environment[
            osetupcons.CoreEnv.SETUP_ATTRS_MODULES
        ].append(odwhcons)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(odwhcons.CoreEnv.ENABLE, None)
        self.environment.setdefault(oenginecons.CoreEnv.ENABLE, None)

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].createGroup(
            group='ovirt_dwh_files',
            description='DWH files',
            optional=True,
        )
        self.logger.debug(
            'dwh version: %s-%s (%s)\n',
            odwhcons.Const.PACKAGE_NAME,
            odwhcons.Const.PACKAGE_VERSION,
            odwhcons.Const.DISPLAY_VERSION,
        )


# vim: expandtab tabstop=4 shiftwidth=4
