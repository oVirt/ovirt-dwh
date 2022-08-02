#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import atexit
import gettext
import os
import random
import string
import tempfile


from otopi import constants as otopicons
from otopi import filetransaction
from otopi import util
from otopi import plugin

from ovirt_engine import configfile
from ovirt_engine import util as outil

from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._sso_config = None
        self._register_sso_client = False
        self._uninstall_files = []
        self._restart_remote_engine = False

    @staticmethod
    def _generatePassword():
        return ''.join([
            random.SystemRandom().choice(
                string.ascii_letters +
                string.digits
            ) for i in range(22)
        ])

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.ADMIN_PASSWORD,
            None
        )
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.CONF_SECRET_KEY,
            self._generatePassword()
        )
        self.environment.setdefault(
            oengcommcons.KeycloakEnv.ENABLE,
            None,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: self.environment[ogdwhcons.CoreEnv.ENABLE],
        before=(
            osetupcons.Stages.DIALOG_TITLES_S_MISC,
        ),
        after=(
            oengcommcons.Stages.NETWORK_OWNERS_CONFIG_CUSTOMIZED,
        ),
    )
    def _customization_url(self):
        self._grafana_url = 'https://{grafana_fqdn}{path}/'.format(
            grafana_fqdn=self.environment[
                ogdwhcons.ConfigEnv.GRAFANA_FQDN
            ],
            path=ogdwhcons.Const.GRAFANA_URI_PATH,
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
            self.environment[ogdwhcons.ConfigEnv.ADMIN_PASSWORD] is None and
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE]
        ),
    )
    def _customization_admin_password(self):
        password = None
        if self.environment.get(oenginecons.ConfigEnv.ADMIN_PASSWORD):
            use_engine_admin_password = dialog.queryBoolean(
                dialog=self.dialog,
                name='GRAFANA_USE_ENGINE_ADMIN_PASSWORD',
                note=_(
                    'Use Engine admin password as initial Grafana admin '
                    'password (@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                default=True
            )
            if use_engine_admin_password:
                password = self.environment[
                    oenginecons.ConfigEnv.ADMIN_PASSWORD
                ]
        if password is None:
            password = dialog.queryPassword(
                dialog=self.dialog,
                logger=self.logger,
                env=self.environment,
                key=ogdwhcons.ConfigEnv.ADMIN_PASSWORD,
                note=_(
                    'Grafana admin password: '
                ),
            )
        self.environment[ogdwhcons.ConfigEnv.ADMIN_PASSWORD] = password

    def _get_sso_client_registration_cmd(self, tmpconf):
        return (
            '/usr/bin/ovirt-register-sso-client-tool '
            '--callback-prefix-url='
            '{grafana_url} '
            '--client-ca-location={ca_pem} '
            '--client-id={client_id} '
            '--encrypted-userinfo=false '
            '--conf-file-name={tmpconf}'
        ).format(
            grafana_url=self._grafana_url,
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

    def _get_engine_access_config(self):
        return (
            'ENGINE_GRAFANA_FQDN={fqdn}\n'
            'ENGINE_GRAFANA_BASE_URL='
            'https://${{ENGINE_GRAFANA_FQDN}}/{uri_path}/\n'
        ).format(
            fqdn=self.environment[ogdwhcons.ConfigEnv.GRAFANA_FQDN],
            uri_path=ogdwhcons.Const.GRAFANA_URI_PATH,
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_LATE_SETUP,
        # env[REMOTE_ENGINE] is created in common engine-setup code,
        # in STAGE_SETUP. So here in STAGE_LATE_SETUP is good enough.
    )
    def _late_setup_remote_engine(self):
        self._remote_engine = self.environment[
            osetupcons.CoreEnv.REMOTE_ENGINE
        ]

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_MISC,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_MISC,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE]
        ),
    )
    def _customization_sso(self):
        if self.environment[oenginecons.CoreEnv.ENABLE]:
            self._register_sso_client = True
        else:
            fd, tmpconf = tempfile.mkstemp()
            atexit.register(os.unlink, tmpconf)
            cmd = self._get_sso_client_registration_cmd(tmpconf)
            self._remote_engine.execute_on_engine(
                cmd=cmd,
                timeout=120,
                text=_(
                    'Please run the following command on the engine machine '
                    '{engine_fqdn}:\n'
                    '{cmd}\n'
                ).format(
                    engine_fqdn=self.environment[
                        oenginecons.ConfigEnv.ENGINE_FQDN
                    ],
                    cmd=cmd,
                ),
            )
            res = self._remote_engine.copy_from_engine(
                file_name=tmpconf,
                dialog_name='PROMPT_GRAFANA_REMOTE_ENGINE_SSO',
            )
            self._restart_remote_engine = dialog.queryBoolean(
                dialog=self.dialog,
                name='GRAFANA_RESTART_REMOTE_ENGINE_FOR_SSO',
                note=_(
                    'The engine should be restarted for Single-Sign-On (SSO) '
                    'to work. Do this as part of Setup? If not, you will have '
                    'to do this later by yourself '
                    '(@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                default=True,
            )
            with open(tmpconf, 'wb') as f:
                f.write(res)
            self._process_sso_client_registration_result(tmpconf)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=ogdwhcons.Stages.GRAFANA_CONFIG,
        after=(
            oengcommcons.Stages.DB_CREDENTIALS_WRITTEN,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            (
                self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE] or
                (
                    self.environment[oengcommcons.KeycloakEnv.ENABLE] and
                    not self.environment[oengcommcons.KeycloakEnv.CONFIGURED]
                )
            )
        )
    )
    def _misc_grafana_config(self):
        if self._register_sso_client:
            fd, tmpconf = tempfile.mkstemp()
            atexit.register(os.unlink, tmpconf)
            self.execute(
                self._get_sso_client_registration_cmd(
                    tmpconf
                ).split(' ')
            )
            self._process_sso_client_registration_result(tmpconf)

        self._uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_grafana_files',
            fileList=self._uninstall_files,
        )
        substitutions = {
            '@ADMIN_PASSWORD@': self.environment[
                ogdwhcons.ConfigEnv.ADMIN_PASSWORD
            ],
            '@PROVISIONING@':
                ogdwhcons.FileLocations.
                    GRAFANA_PROVISIONING_CONFIGURATION,
            '@GRAFANA_PORT@': self.environment[
                ogdwhcons.ConfigEnv.GRAFANA_PORT
            ],
            '@SECRET_KEY@': self.environment[
                ogdwhcons.ConfigEnv.CONF_SECRET_KEY
            ],
            '@GRAFANA_STATE_DIR@': ogdwhcons.FileLocations.GRAFANA_STATE_DIR,
            '@GRAFANA_DB@': ogdwhcons.FileLocations.GRAFANA_DB,
            '@ROOT_URL@': '%s' % self._grafana_url,
            '@GRAFANA_TLS_CLIENT_CA@': oengcommcons.FileLocations.
                OVIRT_ENGINE_PKI_APACHE_CA_CERT,
        }

        fqdn = self.environment[
            oenginecons.ConfigEnv.ENGINE_FQDN
        ]
        auth_url = f'https://{fqdn}/ovirt-engine/sso/openid/authorize'
        token_url = f'https://{fqdn}/ovirt-engine/sso/openid/token'
        api_url = f'https://{fqdn}/ovirt-engine/sso/openid/userinfo'
        scopes = 'ovirt-app-admin,ovirt-app-portal,' \
                 'ovirt-ext=auth:sequence-priority=~'
        role_attr = ''

        # override  configuration for internal Keycloak based SSO
        keycloak_enabled = self.environment.get(oengcommcons.KeycloakEnv.ENABLE)
        keycloak_configured = self.environment.get(oengcommcons.KeycloakEnv.CONFIGURED)

        if keycloak_enabled and not keycloak_configured:
            auth_url = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_AUTH_URL
            ]
            token_url = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_TOKEN_URL
            ]
            api_url = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_USERINFO_URL
            ]
            scopes = f'openid,{scopes}'
            client_id = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_OVIRT_INTERNAL_CLIENT_ID
            ]
            client_secret = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_OVIRT_INTERNAL_CLIENT_SECRET
            ]
            admin_role = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_GRAFANA_ADMIN_ROLE
            ]
            editor_role = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_GRAFANA_EDITOR_ROLE
            ]
            viewer_role = self.environment[
                oengcommcons.KeycloakEnv.KEYCLOAK_GRAFANA_VIEWER_ROLE
            ]
            role_attr = f"\"contains(realm_access.roles[*], " \
                        f"'{admin_role}') && 'Admin' " \
                        f"|| contains(realm_access.roles[*], " \
                        f"'{editor_role}') && 'Editor' " \
                        f"|| contains(realm_access.roles[*], " \
                        f"'{viewer_role}') && 'Viewer'\""
        else:
            client_id = self._sso_config.get('SSO_CLIENT_ID')
            client_secret = self._sso_config.get('SSO_CLIENT_SECRET')

        substitutions['@SSO_AUTH_URL@'] = auth_url
        substitutions['@SSO_TOKEN_URL@'] = token_url
        substitutions['@SSO_API_URL@'] = api_url
        substitutions['@SCOPES@'] = scopes
        substitutions['@OVIRT_GRAFANA_SSO_CLIENT_ID@'] = client_id
        substitutions['@OVIRT_GRAFANA_SSO_CLIENT_SECRET@'] = client_secret
        substitutions['@ROLE_ATTRIBUTE_PATH@'] = role_attr

        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    ogdwhcons.FileLocations.
                    GRAFANA_CONFIG_FILE
                ),
                mode=0o640,
                owner='root',
                group='grafana',
                enforcePermissions=True,
                content=outil.processTemplate(
                    template=(
                        ogdwhcons.FileLocations.
                        GRAFANA_CONFIG_FILE_TEMPLATE
                    ),
                    subst=substitutions,
                ),
                modifiedList=self._uninstall_files,
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            oengcommcons.Stages.DB_CREDENTIALS_WRITTEN,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            self.environment[oenginecons.CoreEnv.ENABLE]
        ),
    )
    def _misc_engine_grafana_access(self):
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    ogdwhcons.FileLocations.
                    OVIRT_ENGINE_SERVICE_CONFIG_GRAFANA
                ),
                mode=0o640,
                owner='root',
                group=self.environment[osetupcons.SystemEnv.GROUP_ENGINE],
                enforcePermissions=True,
                content=self._get_engine_access_config(),
                modifiedList=self._uninstall_files,
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        after=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            not self.environment[oenginecons.CoreEnv.ENABLE]
        ),
    )
    def _closeup_engine_grafana_access(self):
        self._remote_engine.copy_to_engine(
            file_name=(
                ogdwhcons.FileLocations.
                OVIRT_ENGINE_SERVICE_CONFIG_GRAFANA
            ),
            content=self._get_engine_access_config(),
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_SUMMARY,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ]
        ),
    )
    def _closeup_inform_UI(self):
        self.dialog.note(
            text=_(
                'Web access for grafana is enabled at:\n'
                '    {url}\n'
            ).format(
                url=self._grafana_url,
            )
        )
        cmd = 'systemctl restart ovirt-engine'
        cmd_msg = _(
            'Please run the following command on the engine machine '
            '{engine_fqdn}, for SSO to work:\n'
            '{cmd}\n'
        ).format(
            engine_fqdn=self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
            ],
            cmd=cmd,
        )
        if self._restart_remote_engine:
            self._remote_engine.execute_on_engine(
                cmd=cmd,
                timeout=120,
                text=cmd_msg,
            )
        else:
            self.dialog.note(
                text=cmd_msg,
            )


# vim: expandtab tabstop=4 shiftwidth=4
