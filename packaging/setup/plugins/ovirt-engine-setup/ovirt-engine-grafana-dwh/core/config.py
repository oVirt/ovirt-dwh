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

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            osetupcons.Stages.DIALOG_TITLES_S_MISC,
        ),
        after=(
            osetupcons.Stages.CONFIG_PROTOCOLS_CUSTOMIZATION,
        ),
    )
    def _customization_url(self):
        # TODO: Fix for separate machines
        self._grafana_url = 'https://{grafana_fqdn}{path}/'.format(
            grafana_fqdn=self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
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
        if self.environment[oenginecons.ConfigEnv.ADMIN_PASSWORD]:
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
        sso_client_tool = '/usr/bin/ovirt-register-sso-client-tool'
        if not os.path.exists(sso_client_tool):
            # TODO: make this optional
            # After grafana supports split config files, have sso in its
            # own file
            raise RuntimeError(_('{tool} is missing').format(sso_client_tool))

        return (
            '{tool} '
            '--callback-prefix-url='
            '{grafana_url} '
            '--client-ca-location={ca_pem} '
            '--client-id={client_id} '
            '--encrypted-userinfo=false '
            '--conf-file-name={tmpconf}'
        ).format(
            tool=sso_client_tool,
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
            # TODO: do this with remote_engine
            dialog.queryString(
                name='PROMPT_GRAFANA_REMOTE_ENGINE_SSO',
                note=_(
                    'Please run the following command on the engine machine '
                    '{engine_fqdn}:\n'
                    '{cmd}\n'
                    'Then copy the file {tmpconf} from the engine machine to '
                    'this machine, and press Enter to continue: '
                ).format(
                    engine_fqdn=self.environment[
                        oenginecons.ConfigEnv.ENGINE_FQDN
                    ],
                    cmd=self._get_sso_client_registration_cmd(tmpconf),
                    tmpconf=tmpconf,
                ),
                prompt=True,
                default='y',  # Allow Enter without any value
            )
            self._process_sso_client_registration_result(tmpconf)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        after=(
            oengcommcons.Stages.DB_CREDENTIALS_WRITTEN,
        ),
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE]
        ),
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

        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_grafana_files',
            fileList=uninstall_files,
        )
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
                    subst={
                        '@ADMIN_PASSWORD@': self.environment[
                            ogdwhcons.ConfigEnv.ADMIN_PASSWORD
                        ],
                        '@PROVISIONING@': (
                            ogdwhcons.FileLocations.
                            GRAFANA_PROVISIONING_CONFIGURATION
                        ),
                        '@GRAFANA_PORT@': self.environment[
                            ogdwhcons.ConfigEnv.GRAFANA_PORT
                        ],
                        '@SECRET_KEY@': self.environment[
                            ogdwhcons.ConfigEnv.CONF_SECRET_KEY
                        ],
                        '@GRAFANA_STATE_DIR@': (
                            ogdwhcons.FileLocations.GRAFANA_STATE_DIR
                        ),
                        '@GRAFANA_DB@': (
                            ogdwhcons.FileLocations.GRAFANA_DB
                        ),
                        '@OVIRT_GRAFANA_SSO_CLIENT_ID@': self._sso_config.get(
                            'SSO_CLIENT_ID'
                        ),
                        '@OVIRT_GRAFANA_SSO_CLIENT_SECRET@': (
                            self._sso_config.get('SSO_CLIENT_SECRET')
                        ),
                        '@ENGINE_SSO_AUTH_URL@': (
                            'https://{fqdn}/ovirt-engine/sso'.format(
                                fqdn=self.environment[
                                    oenginecons.ConfigEnv.ENGINE_FQDN
                                ],
                            )
                        ),
                        '@ROOT_URL@': '%s' % self._grafana_url,
                    },
                ),
                modifiedList=uninstall_files,
            )
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


# vim: expandtab tabstop=4 shiftwidth=4
