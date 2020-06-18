#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Config plugin."""


from otopi import filetransaction
from otopi import plugin
from otopi import util
from otopi import constants as otopicons

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


@util.export
class Plugin(plugin.PluginBase):
    """Config plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._config = ogdwhcons.FileLocations.GRAFANA_CONFIG_FILE

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[
            osetupcons.RenameEnv.FILES_TO_BE_MODIFIED
        ].append(self._config)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
    )
    def _misc(self):
        uninstall_files = []

        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].createGroup(
            group='ovirt_grafana_files',
            description='Grafana files',
            optional=True,
        ).addFiles(
            group='ovirt_grafana_files',
            fileList=uninstall_files,
        )
        generic_auth_replacements = {
            'auth_url': '/ovirt-engine/sso/openid/authorize',
            'token_url': '/ovirt-engine/sso/openid/token',
            'api_url': '/ovirt-engine/sso/openid/userinfo',
        }
        with open(self._config, 'r') as f:
            content = []
            inside_generic_auth = False
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('[') and inside_generic_auth:
                    inside_generic_auth = False
                if '[auth.generic_oauth]' == line:
                    inside_generic_auth = True
                if line.startswith('root_url'):
                    line = 'root_url = https://{fqdn}{path}/'.format(
                        fqdn=self.environment[osetupcons.RenameEnv.FQDN],
                        path=ogdwhcons.Const.GRAFANA_URI_PATH,
                    )
                elif line and inside_generic_auth:
                    key = line.split()[0]
                    if key in generic_auth_replacements:
                        line = '{key} = https://{fqdn}{path}'.format(
                            key=key,
                            fqdn=self.environment[osetupcons.RenameEnv.FQDN],
                            path=generic_auth_replacements[key],
                        )
                content.append(line)

        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=self._config,
                content=content,
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
