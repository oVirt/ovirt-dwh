#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Connection plugin."""


import gettext


from otopi import constants as otopicons
from otopi import transaction
from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Connection plugin."""

    class DBTransaction(transaction.TransactionElement):
        """yum transaction element."""

        def __init__(self, parent):
            self._parent = parent

        def __str__(self):
            return _("DWH database Transaction")

        def prepare(self):
            pass

        def abort(self):
            connection = self._parent.environment[odwhcons.DBEnv.CONNECTION]
            if connection is not None:
                connection.rollback()
                self._parent.environment[odwhcons.DBEnv.CONNECTION] = None

        def commit(self):
            connection = self._parent.environment[odwhcons.DBEnv.CONNECTION]
            if connection is not None:
                connection.commit()

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            self.DBTransaction(self)
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        name=odwhcons.Stages.DB_CONNECTION_CUSTOMIZATION,
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ] and not self.environment[
            odwhcons.ProvisioningEnv.POSTGRES_PROVISIONING_ENABLED
        ],
        before=(
            oengcommcons.Stages.DB_OWNERS_CONNECTIONS_CUSTOMIZED,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_DATABASE,
        ),
    )
    def _customization(self):
        dbovirtutils = database.OvirtUtils(
            plugin=self,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        )
        dbovirtutils.getCredentials(
            name='DWH',
            queryprefix='OVESETUP_DWH_DB_',
            defaultdbenvkeys=odwhcons.Const.DEFAULT_DWH_DB_ENV_KEYS,
            show_create_msg=True,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=odwhcons.Stages.DB_CONNECTION_AVAILABLE,
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
        after=(
            odwhcons.Stages.DB_SCHEMA,
        ),
    )
    def _connection(self):
        self.environment[
            odwhcons.DBEnv.STATEMENT
        ] = database.Statement(
            environment=self.environment,
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
        )
        # must be here as we do not have database at validation
        self.environment[
            odwhcons.DBEnv.CONNECTION
        ] = self.environment[odwhcons.DBEnv.STATEMENT].connect()


# vim: expandtab tabstop=4 shiftwidth=4
