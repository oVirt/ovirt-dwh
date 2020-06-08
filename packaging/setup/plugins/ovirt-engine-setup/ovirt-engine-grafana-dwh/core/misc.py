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
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_setup_lib import dialog


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
            ogdwhcons.ConfigEnv.GRAFANA_USER,
            ogdwhcons.Defaults.GRAFANA_DEFAULT_USER
        )
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.GRAFANA_GROUP,
            ogdwhcons.Defaults.GRAFANA_DEFAULT_GROUP
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        name=ogdwhcons.Stages.CORE_ENABLE,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_PRODUCT_OPTIONS,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_PRODUCT_OPTIONS,
            oenginecons.Stages.CORE_ENABLE
        ),
    )
    def _customization_enable_grafana(self):
        if self.environment[ogdwhcons.CoreEnv.ENABLE] is None:
            self.environment[
                ogdwhcons.CoreEnv.ENABLE
            ] = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_GRAFANA_ENABLE',
                note=_(
                    'Configure Grafana on this host '
                    '(@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                default=True,
            )
        if self.environment[ogdwhcons.CoreEnv.ENABLE]:
            self.environment[
                ogdwhcons.ConfigEnv.GRAFANA_SERVICE_STOP_NEEDED
            ] = True


# vim: expandtab tabstop=4 shiftwidth=4
