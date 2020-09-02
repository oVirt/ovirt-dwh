#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Config plugin."""

import atexit
import gettext
import os
import tempfile

from otopi import filetransaction
from otopi import plugin
from otopi import util
from otopi import constants as otopicons

from ovirt_engine import configfile

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_engine_setup.engine import constants as oenginecons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Config plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._sso_config = None
        self._register_sso_client = False
        self._config = ogdwhcons.FileLocations.GRAFANA_CONFIG_FILE
        self._engine_config = (
            ogdwhcons.FileLocations.
            OVIRT_ENGINE_SERVICE_CONFIG_GRAFANA
        )
        self._uninstall_files = []

    def _get_sso_client_registration_cmd(self, tmpconf):
        url = 'https://{grafana_fqdn}{path}/'.format(
            grafana_fqdn=self.environment[
                ogdwhcons.ConfigEnv.GRAFANA_FQDN
            ],
            path=ogdwhcons.Const.GRAFANA_URI_PATH,
        )
        return (
            '/usr/bin/ovirt-register-sso-client-tool '
            '--callback-prefix-url='
            '{grafana_url} '
            '--client-ca-location={ca_pem} '
            '--client-id={client_id} '
            '--encrypted-userinfo=false '
            '--conf-file-name={tmpconf}'
        ).format(
            grafana_url=url,
            ca_pem=oenginecons.FileLocations.OVIRT_ENGINE_PKI_ENGINE_CA_CERT,
            client_id=ogdwhcons.Const.OVIRT_GRAFANA_SSO_CLIENT_ID,
            tmpconf=tmpconf,
        )

    def _process_sso_client_registration_result(self, tmpconf):
        self._sso_config = configfile.ConfigFile([tmpconf])
        self.environment[
            otopicons.CoreEnv.LOG_FILTER
        ].append(
            self._sso_config.get(
                'SSO_CLIENT_SECRET'
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup(self):
        self.environment[
            osetupcons.RenameEnv.FILES_TO_BE_MODIFIED
        ].extend((
            self._config,
            self._engine_config,
        ))
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].createGroup(
            group='ovirt_grafana_files',
            description='Grafana files',
            optional=True,
        ).addFiles(
            group='ovirt_grafana_files',
            fileList=self._uninstall_files,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_MISC,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_MISC,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE]
        ),
    )
    def _customization_sso(self):
        if self.environment[oenginecons.CoreEnv.ENABLE]:
            self._register_sso_client = True
        else:
            # TODO handle separate machines
            raise RuntimeError(_(
                'rename on separate Grafana machine is not supported'
            ))

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE]
        ),
    )
    def _misc(self):
        generic_auth_replacements = {
            'auth_url': '/ovirt-engine/sso/openid/authorize',
            'token_url': '/ovirt-engine/sso/openid/token',
            'api_url': '/ovirt-engine/sso/openid/userinfo',
        }
        if self._register_sso_client:
            fd, tmpconf = tempfile.mkstemp()
            atexit.register(os.unlink, tmpconf)
            self.execute(
                self._get_sso_client_registration_cmd(
                    tmpconf
                ).split(' ')
            )
            self._process_sso_client_registration_result(tmpconf)

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
                if line.startswith('client_secret') and inside_generic_auth:
                    self._sso_config.get('SSO_CLIENT_SECRET')
                    line = 'client_secret = {secret}'.format(
                        secret=self._sso_config.get('SSO_CLIENT_SECRET'),
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
                modifiedList=self._uninstall_files,
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE]
        ),
    )
    def _engine_config_misc(self):
        with open(self._engine_config, 'r') as f:
            content = []
            for line in f:
                if line.startswith('ENGINE_GRAFANA_FQDN='):
                    line = 'ENGINE_GRAFANA_FQDN={fqdn}'.format(
                        fqdn=self.environment[osetupcons.RenameEnv.FQDN],
                    )
                content.append(line)

        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=self._engine_config,
                content=content,
                modifiedList=self._uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
