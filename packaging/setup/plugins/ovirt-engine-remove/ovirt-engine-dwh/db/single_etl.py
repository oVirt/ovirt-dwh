#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import dwh_history_timekeeping as \
    engine_db_timekeeping


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            oenginecons.RemoveEnv.REMOVE_ENGINE_DATABASE,
            False,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            odwhcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        ),
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            not self.environment[oenginecons.RemoveEnv.REMOVE_ENGINE_DATABASE]
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
        except Exception as e:
            self.logger.debug('exception', exc_info=True)
            self.logger.warning(
                _(
                    'Cannot update Engine database: {error}'
                ).format(
                    error=e,
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
