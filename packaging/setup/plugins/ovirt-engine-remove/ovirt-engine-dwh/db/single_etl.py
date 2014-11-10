#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2014 Red Hat, Inc.
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


import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-dwh')


from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.dwh import engine_db_timekeeping


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.RemoveEnv.REMOVE_ENGINE_DATABASE,
            False,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        ),
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            not self.environment[odwhcons.RemoveEnv.REMOVE_ENGINE_DATABASE]
        ),
    )
    def _misc(self):
        try:
            statement = self.environment[odwhcons.EngineDBEnv.STATEMENT]
            db_dwh_uuid = engine_db_timekeeping.getValueFromTimekeeping(
                statement=statement,
                name=engine_db_timekeeping.DB_KEY_UUID
            )
            if self.environment[odwhcons.CoreEnv.UUID] != db_dwh_uuid:
                self.logger.debug('_ is %s' % _)
                self.logger.warning(
                    _(
                        'Not updating engine database to disconnect from dwh '
                        '- seems like a different dwh was already setup for it'
                    )
                )
            else:
                engine_db_timekeeping.updateValueInTimekeeping(
                    statement=statement,
                    name=engine_db_timekeeping.DB_KEY_HOSTNAME,
                    value=''
                )
                engine_db_timekeeping.updateValueInTimekeeping(
                    statement=statement,
                    name=engine_db_timekeeping.DB_KEY_UUID,
                    value=''
                )
        except RuntimeError as e:
            self.logger.debug('exception', exc_info=True)
            self.logger.warning(
                _(
                    'Cannot update Engine database: {error}'
                ).format(
                    error=e,
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
