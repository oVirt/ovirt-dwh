#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2014-2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Database plugin."""


from otopi import util
from otopi import plugin


from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine_common import dwh_history_timekeeping as \
    engine_db_timekeeping
from ovirt_engine_setup.dwh import constants as odwhcons


@util.export
class Plugin(plugin.PluginBase):
    """Database plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        ),
    )
    def _misc(self):
        engine_db_timekeeping.updateValueInTimekeeping(
            statement=self.environment[oenginecons.EngineDBEnv.STATEMENT],
            name=engine_db_timekeeping.DB_KEY_HOSTNAME,
            value=self.environment[osetupcons.RenameEnv.FQDN]
        )


# vim: expandtab tabstop=4 shiftwidth=4
