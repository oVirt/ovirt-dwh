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
        stage=plugin.Stages.STAGE_BOOT,
        before=(
            osetupcons.Stages.SECRETS_FILTERED_FROM_SETUP_ATTRS_MODULES,
        ),
    )
    def _boot(self):
        self.environment[
            osetupcons.CoreEnv.SETUP_ATTRS_MODULES
        ].append(
            ogdwhcons,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(ogdwhcons.CoreEnv.ENABLE, None)
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.GRAFANA_DB_CREATED_BY_US,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].createGroup(
            group='ovirt_grafana_files',
            description='Grafana files',
            optional=True,
        )


# vim: expandtab tabstop=4 shiftwidth=4
