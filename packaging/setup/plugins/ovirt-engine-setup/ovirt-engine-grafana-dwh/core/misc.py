#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import plugin

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    def _configure_grafana_default(self):
        # We used to configure grafana by default.
        # This broke upgrade/restore of hosted-engine from 4.3 if the
        # backed up engine was set up with a remote DWH database[1].
        # To fix this, we kept the default here to True, but patched
        # the appliance to override this to False, unconditionally.
        # This means that hosted-engine setups never configured grafana
        # out-of-the-box, and always required configuring it manually
        # later if needed.
        # I am going to revert that patch to the appliance, and instead
        # make the default here slightly more complex.
        # [1] https://bugzilla.redhat.com/show_bug.cgi?id=1866780
        if (
            not self.environment[odwhcons.DBEnv.NEW_DATABASE]
            and self.environment[odwhcons.DBEnv.HOST] != 'localhost'
            and self.environment[otopicons.DialogEnv.AUTO_ACCEPT_DEFAULT]
        ):
            return False
        return True


    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        name=ogdwhcons.Stages.CORE_ENABLE,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_PRODUCT_OPTIONS,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_PRODUCT_OPTIONS,
            # No real need to ask after asking about the engine/DWH, but it
            # seems more sensible.
            oenginecons.Stages.CORE_ENABLE,
            odwhcons.Stages.CORE_ENABLE,
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
                default=self._configure_grafana_default(),
            )
        if self.environment[ogdwhcons.CoreEnv.ENABLE]:
            self.environment[oengcommcons.ApacheEnv.ENABLE] = True
            self.environment[
                ogdwhcons.ConfigEnv.GRAFANA_SERVICE_STOP_NEEDED
            ] = True


# vim: expandtab tabstop=4 shiftwidth=4
