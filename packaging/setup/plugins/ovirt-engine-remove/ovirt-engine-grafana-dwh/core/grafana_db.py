#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import datetime
import gettext
import os


from otopi import util
from otopi import plugin


from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: self.environment[
            ogdwhcons.ConfigEnv.GRAFANA_DB_CREATED_BY_US
        ],
    )
    def _closeup_remove_grafana_db(self):
        db = os.path.join(
            ogdwhcons.FileLocations.GRAFANA_STATE_DIR,
            ogdwhcons.FileLocations.GRAFANA_DB
        )
        backup = '%s.%s' % (
            db,
            datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        )
        try:
            os.rename(db, backup)
            self.logger.info(
                'Grafana database %s renamed to %s',
                db,
                backup
            )
        except FileNotFoundError:
            self.logger.debug('%s not found, not moving', db)


# vim: expandtab tabstop=4 shiftwidth=4
