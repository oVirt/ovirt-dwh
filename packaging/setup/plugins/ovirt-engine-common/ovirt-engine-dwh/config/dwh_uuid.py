#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import uuid


from otopi import util
from otopi import plugin


from ovirt_engine import configfile


from ovirt_engine_setup.dwh import constants as odwhcons


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.CoreEnv.UUID,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        config = configfile.ConfigFile([
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DEFAULTS,
            odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIG,
        ])
        self.environment[
            odwhcons.CoreEnv.UUID
        ] = config.get('DWH_UUID') or str(uuid.uuid4())


# vim: expandtab tabstop=4 shiftwidth=4
