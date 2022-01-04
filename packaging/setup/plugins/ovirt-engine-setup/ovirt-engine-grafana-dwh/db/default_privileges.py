#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Grafana default privileges plugin."""


import gettext

from otopi import plugin
from otopi import util

from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Grafana default privileges plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = True

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        before=(
            odwhcons.Stages.DB_SCHEMA,
        ),
        after=(
            odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
            ogdwhcons.Stages.DB_PROVISIONING_CREATE_USER,
        ),
        condition=lambda self: self.environment[ogdwhcons.CoreEnv.ENABLE],
    )
    def _misc_set_default_privileges(self):
        database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        ).setDefaultPrivilegesReadOnlyForUser(
            user=self.environment[ogdwhcons.GrafanaDBEnv.USER],
        )


# vim: expandtab tabstop=4 shiftwidth=4
