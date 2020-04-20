#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2020 Red Hat, Inc.
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
        os.rename(db, backup)
        self.logger.info(
            'Grafana database %s renamed to %s',
            db,
            backup
        )


# vim: expandtab tabstop=4 shiftwidth=4
