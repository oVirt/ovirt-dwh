#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Connection plugin."""


import gettext


from otopi import util
from otopi import plugin

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Connection plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ] and not self.environment.get(
            oengcommcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED
        ),
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
            oengcommcons.Stages.DB_OWNERS_CONNECTIONS_CUSTOMIZED,
        ),
    )
    def _engine_customization(self):
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
        )
        dbovirtutils.getCredentials(
            name='Engine',
            defaultdbenvkeys={
                'host': '',
                'port': '5432',
                'secured': '',
                'hostValidation': False,
                'user': 'engine',
                'password': None,
                'database': 'engine',
            },
            show_create_msg=False,
            credsfile=(
                odwhcons.FileLocations.
                OVIRT_ENGINE_ENGINE_SERVICE_CONFIG_DATABASE
            ),
        )


# vim: expandtab tabstop=4 shiftwidth=4
