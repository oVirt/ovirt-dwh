#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""DB pgpass plugin."""


import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """DB pgpass plugin."""
    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment[odwhcons.DBEnv.PGPASS_FILE] = None

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            self.environment[odwhcons.DBEnv.PASSWORD] is not None
        ),
    )
    def _misc(self):
        database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        ).createPgPass()


# vim: expandtab tabstop=4 shiftwidth=4
