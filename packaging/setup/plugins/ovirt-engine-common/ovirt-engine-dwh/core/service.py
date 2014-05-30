#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013 Red Hat, Inc.
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


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import dwhconstants as odwhcons


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_TRANSACTION_BEGIN,
        before=(
            osetupcons.Stages.SYSTEM_HOSTILE_SERVICES_DETECTION,
        ),
        condition=lambda self: not self.environment[
            osetupcons.CoreEnv.DEVELOPER_MODE
        ],
    )
    def _transactionBegin(self):
        if self.services.exists(name=odwhcons.Const.SERVICE_NAME):
            self.logger.info(_('Stopping dwh service'))
            self.services.state(
                name=odwhcons.Const.SERVICE_NAME,
                state=False
            )


# vim: expandtab tabstop=4 shiftwidth=4
