#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Engine FQDN plugin."""


from otopi import util
from otopi import plugin

from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine import constants as oenginecons

@util.export
class Plugin(plugin.PluginBase):
    """Engine FQDN plugin."""

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.DB_CONNECTION_AVAILABLE,
        ),
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ]
    )
    def _save_engine_fqdn(self):
        # Check that the engine fqdn exists
        if self.environment[oenginecons.ConfigEnv.ENGINE_FQDN] is not None:
            # Check if the engine fqdn changed
            fqdn_result = self.environment[odwhcons.DBEnv.STATEMENT].execute(
                statement="""
                    select var_value
                    from history_configuration
                    where var_name = 'EngineFQDN'
                """
            )
            # Inform the user if we are going to modify the engine fqdn
            if (len(fqdn_result) > 0 and
                fqdn_result != self.environment[oenginecons.ConfigEnv.ENGINE_FQDN]):
                self.dialog.note(
                    text=(
                        'Updating the engine FQDN in the Data Warehouse Database.'
                    )
                )
            self.environment[
                odwhcons.DBEnv.STATEMENT
            ].execute(
            # The query adds the fqdn to the db.
            # If the value exists it will update it,
            # whether it is different from the old value or not.
                statement="""
                    insert into history_configuration (var_name, var_value)
                    values ('EngineFQDN', %(engine_fqdn)s)
                    on conflict (var_name) do update
                    set var_value = EXCLUDED.var_value
                """,
                args=dict(
                    engine_fqdn= self.environment[
                        oenginecons.ConfigEnv.ENGINE_FQDN
                    ],
                )
            )
# vim: expandtab tabstop=4 shiftwidth=4
