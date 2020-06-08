#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Grafana connection plugin."""


import gettext

from otopi import plugin
from otopi import util

from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Grafana connection plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = True

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        name=ogdwhcons.Stages.DB_GRAFANA_CONNECTION_CUSTOMIZATION,
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            oengcommcons.Stages.DB_OWNERS_CONNECTIONS_CUSTOMIZED,
        ),
        condition=lambda self: self.environment[ogdwhcons.CoreEnv.ENABLE],
    )
    def _customization(self):
        database.OvirtUtils(
            plugin=self,
            dbenvkeys=ogdwhcons.Const.GRAFANA_DB_ENV_KEYS,
        ).getCredentials(
            name='Grafana',
            queryprefix='OVESETUP_GRAFANA_DB_',
            defaultdbenvkeys=ogdwhcons.Const.DEFAULT_GRAFANA_DB_ENV_KEYS,
            show_create_msg=False,
            validateconf=False,
        )


# vim: expandtab tabstop=4 shiftwidth=4
