#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2016 Red Hat, Inc.
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


from otopi import util
from otopi import plugin


from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import util as osetuputil
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.dwh import constants as odwhcons


from ovirt_setup_lib import hostname as osetuphostname


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
            oenginecons.ConfigEnv.ENGINE_FQDN,
            None
        )
        self.environment.setdefault(
            odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED,
            False
        )
        self._enabled = False
        self._configured_now = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_NETWORK,
            oengcommcons.Stages.NETWORK_OWNERS_CONFIG_CUSTOMIZED,
        ),
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_NETWORK,
        ),
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ] and not self.environment[
            oenginecons.CoreEnv.ENABLE
        ] and not self.environment[
            odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED
        ],
    )
    def _remote_engine_customization(self):
        self._enabled = True
        osetuphostname.Hostname(
            plugin=self,
        ).getHostname(
            envkey=oenginecons.ConfigEnv.ENGINE_FQDN,
            whichhost=_('the engine'),
            supply_default=False,
        )
        self._remote_engine = self.environment[
            osetupcons.CoreEnv.REMOTE_ENGINE
        ]
        self._remote_engine.configure(
            fqdn=self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
            ],
        )

        # It's actually configured only at closeup, but postinstall is
        # written at misc, so set here, earlier.
        self.environment[odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED] = True

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_SUMMARY,
        ),
        condition=lambda self: self._enabled,
    )
    def _closeupEngineAccess(self):
        # Doing this at closeup and not misc, because if using
        # remote_engine style manual_files, we prompt the user,
        # which might take a long time (until the user notices
        # and handles), and we'd rather not block the transaction
        # waiting. Downside is that if we fail during closeup
        # but before this event, it will not run, also on next
        # attempt.
        with open(
            odwhcons.FileLocations.
            OVIRT_ENGINE_ENGINE_SERVICE_CONFIG_DWH_DATABASE_EXAMPLE
        ) as f:
            self._remote_engine.copy_to_engine(
                file_name=(
                    odwhcons.FileLocations.
                    OVIRT_ENGINE_ENGINE_SERVICE_CONFIG_DWH_DATABASE
                ),
                content=f.read(),
                uid=osetuputil.getUid(
                    self.environment[osetupcons.SystemEnv.USER_ENGINE]
                ),
                gid=osetuputil.getGid(
                    self.environment[osetupcons.SystemEnv.GROUP_ENGINE]
                ),
                mode=0o600,
            )
        self._configured_now = True

    @plugin.event(
        stage=plugin.Stages.STAGE_CLEANUP,
        condition=lambda self: self._enabled and not self._configured_now,
    )
    def _cleanupEngineAccess(self):
        self.logger.warning(
            _(
                'Remote engine was not configured to be able to access '
                'DWH, please check the logs.'
            )
        )

# vim: expandtab tabstop=4 shiftwidth=4
