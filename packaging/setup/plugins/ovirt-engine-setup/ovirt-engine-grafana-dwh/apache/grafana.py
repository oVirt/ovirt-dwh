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


import gettext

from otopi import constants as otopicons
from otopi import filetransaction
from otopi import plugin
from otopi import util

from ovirt_engine import util as outil

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


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
            ogdwhcons.ConfigEnv.HTTPD_CONF_GRAFANA,
            ogdwhcons.FileLocations.HTTPD_CONF_GRAFANA
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ]
        ),
    )
    def _httpd_grafana_misc(self):
        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_grafana_files',
            fileList=uninstall_files,
        )
        self.environment[oengcommcons.ApacheEnv.NEED_RESTART] = True
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=self.environment[
                    ogdwhcons.ConfigEnv.HTTPD_CONF_GRAFANA
                ],
                content=outil.processTemplate(
                    template=(
                        ogdwhcons.FileLocations.
                        HTTPD_CONF_GRAFANA_TEMPLATE
                    ),
                    subst={
                        '@GRAFANA_PORT@': self.environment[
                            ogdwhcons.ConfigEnv.GRAFANA_PORT
                        ],
                        '@GRAFANA_URI_PATH@': ogdwhcons.Const.GRAFANA_URI_PATH,
                    },
                ),
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
