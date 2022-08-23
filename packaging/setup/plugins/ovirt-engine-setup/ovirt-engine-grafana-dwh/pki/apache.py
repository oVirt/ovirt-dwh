#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""apache PKI plugin."""


import contextlib
import gettext
import os
import time
from six.moves.urllib.request import urlopen

from otopi import constants as otopicons
from otopi import filetransaction
from otopi import plugin
from otopi import util

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import remote_engine
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import pki_utils
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons

from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """apache pki plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = False
        self._enrolldata = None
        self._need_ca_cert = False
        self._apache_ca_cert = None

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.PKI_APACHE_CSR_FILENAME,
            None
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            osetupcons.Stages.DIALOG_TITLES_S_NETWORK,
        ),
        after=(
            ogdwhcons.Stages.CORE_ENABLE,
            oenginecons.Stages.CORE_ENABLE,
        ),
        condition=lambda self: (
            self.environment[
                ogdwhcons.CoreEnv.ENABLE
            ] and
            # If on same machine as engine, engine setup creates pki for us
            not self.environment[
                oenginecons.CoreEnv.ENABLE
            ]
        ),
    )
    def _customization_needed(self):
        engine_apache_pki_found = (
            os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_KEY
            ) and os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
            ) and os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT
            )
        )

        renew = False
        if engine_apache_pki_found and pki_utils.ok_to_renew_cert(
            self.logger,
            pki_utils.x509_load_cert(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT,
            ),
            # Normally we'd verify against the CA cert, but we do not keep
            # it in OVIRT_ENGINE_PKI_ENGINE_CA_CERT. So pass the copy we have
            # in OVIRT_ENGINE_PKI_APACHE_CA_CERT . This means that if a user
            # replaced both (which is quite likely), we'd end up not verifying
            # against the engine's CA.
            # TODO: Is this a problem? If so, handle somehow.
            # In practice, it simply means that we might prompt asking whether
            # to renew, even if the user replaced the cert, if it expires.
            # Perhaps that's ok.
            pki_utils.x509_load_cert(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
            ),
            'apache',
            True,
            True,
            self.environment,
        ):
            renew = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_RENEW_GRAFANA_PKI',
                note=_(
                    'The certificate used for HTTPS access to grafana '
                    'should be renewed, '
                    'because it expires soon, or includes an invalid '
                    'expiry date, or was created with validity '
                    'period longer than 398 days, or does not include the '
                    'subjectAltName extension, which can cause it to be '
                    'rejected by recent browsers.\n'
                    'See {url} for more details.\n'
                    'Please note, that renewing the certificate will be done '
                    'using the internal CA. If you replaced the certificate '
                    'with an external CA, you should reply No here and renew '
                    'the certificate using the external CA.\n'
                    'Renew the certificate? '
                    '(@VALUES@) [@DEFAULT@]: '
                ).format(
                    url=self.environment.get(
                        oenginecons.ConfigEnv.PKI_RENEWAL_DOC_URL,
                        'https://ovirt.org/'
                    ),
                ),
                prompt=True,
                default=None,
            )
            if not renew:
                skip_renewal = dialog.queryBoolean(
                    dialog=self.dialog,
                    name='OVESETUP_SKIP_RENEW_PKI_CONFIRM',
                    note=_(
                        'Are you really sure that you want to skip the '
                        'PKI renewal process?\n'
                        'Please notice that recent openssl and gnutls '
                        'upgrades can lead hosts refusing this CA cert '
                        'making them unusable.\n'
                        'If you choose "Yes", setup will continue and you '
                        'will be asked again the next '
                        'time you run this Setup. Otherwise, this process '
                        'will abort and you will be expected to plan a '
                        'proper upgrade according to {url}.\n'
                        'Skip PKI renewal process? '
                        '(@VALUES@) [@DEFAULT@]: '
                    ).format(
                        url=self.environment.get(
                            oenginecons.ConfigEnv.PKI_RENEWAL_DOC_URL,
                            'https://ovirt.org/'
                        ),
                    ),
                    prompt=True,
                    default=False,
                )
                if not skip_renewal:
                    raise RuntimeError('Aborted by user')

        if not engine_apache_pki_found or renew:
            self._enabled = True
            # odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED is saved in
            # postinstall, and was originally used only for DWH itself.
            # If dwh was already configured, but grafana was not, and now
            # the user wants to configure grafana, we need to configure
            # remote_engine again, because we do not save any relevant
            # data for it (e.g. engine fqdh and root password). So clear
            # this here so that the remote_engine plugin will configure
            # it.
            self.environment[
                odwhcons.ConfigEnv.REMOTE_ENGINE_CONFIGURED
            ] = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_PKI,
        ),
        after=(
            oengcommcons.Stages.DIALOG_TITLES_S_PKI,
        ),
        condition=lambda self: self._enabled,
    )
    def _customization(self):
        self._enrolldata = remote_engine.EnrollCert(
            remote_engine=self.environment[
                osetupcons.CoreEnv.REMOTE_ENGINE
            ],
            engine_fqdn=self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
            ],
            base_name=ogdwhcons.Const.PKI_GRAFANA_APACHE_CERT_NAME,
            base_touser=_('Apache'),
            key_file=(
                ogdwhcons.FileLocations.
                OVIRT_ENGINE_PKI_GRAFANA_APACHE_KEY
            ),
            cert_file=(
                ogdwhcons.FileLocations.
                OVIRT_ENGINE_PKI_GRAFANA_APACHE_CERT
            ),
            csr_fname_envkey=(
                ogdwhcons.ConfigEnv.PKI_APACHE_CSR_FILENAME
            ),
            engine_ca_cert_file=(
                oenginecons.FileLocations.
                OVIRT_ENGINE_PKI_ENGINE_CA_CERT
            ),
            engine_pki_requests_dir=os.path.join(
                oenginecons.FileLocations.OVIRT_ENGINE_PKIDIR,
                'requests',
            ),
            engine_pki_certs_dir=(
                oenginecons.FileLocations.
                OVIRT_ENGINE_PKICERTSDIR
            ),
            key_size=self.environment[ogdwhcons.ConfigEnv.KEY_SIZE],
            url=(
                "https://ovirt.org/"
                "develop/release-management/features/grafana/grafana.html"
            ),
        )
        self._enrolldata.enroll_cert()

        self._need_ca_cert = not os.path.exists(
            ogdwhcons.FileLocations.
            OVIRT_ENGINE_PKI_GRAFANA_APACHE_CA_CERT
        )

        tries_left = 30
        while (
            self._need_ca_cert and
            self._apache_ca_cert is None and
            tries_left > 0
        ):
            remote_engine_host = self.environment[
                oenginecons.ConfigEnv.ENGINE_FQDN
            ]

            with contextlib.closing(
                urlopen(
                    'http://{engine_fqdn}/ovirt-engine/services/'
                    'pki-resource?resource=ca-certificate&'
                    'format=X509-PEM'.format(
                        engine_fqdn=remote_engine_host
                    )
                )
            ) as urlObj:
                engine_ca_cert = urlObj.read()
                if engine_ca_cert:
                    self._apache_ca_cert = engine_ca_cert
                else:
                    self.logger.error(
                        _(
                            'Failed to get CA Certificate from engine. '
                            'Please check access to the engine and its '
                            'status.'
                        )
                    )
                    time.sleep(10)
                    tries_left -= 1
        if self._need_ca_cert and self._apache_ca_cert is None:
            raise RuntimeError(_('Failed to get CA Certificate from engine'))

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self._enabled
        ),
        after=(
            oenginecons.Stages.CA_AVAILABLE,
            ogdwhcons.Stages.PKI_MISC,
        ),
    )
    def _misc_pki(self):
        self._enrolldata.add_to_transaction(
            uninstall_group_name='ca_pki_grafana',
            uninstall_group_desc='Grafana PKI keys',
        )
        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].createGroup(
            group='ca_pki_grafana',
            description='Grafana PKI keys',
            optional=True,
        ).addFiles(
            group='ca_pki_grafana',
            fileList=uninstall_files,
        )
        if not os.path.exists(
            oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT
        ):
            os.symlink(
                ogdwhcons.FileLocations.
                OVIRT_ENGINE_PKI_GRAFANA_APACHE_CERT,
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT
            )
            uninstall_files.append(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT
            )
        if not os.path.exists(
            oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_KEY
        ):
            os.symlink(
                ogdwhcons.FileLocations.OVIRT_ENGINE_PKI_GRAFANA_APACHE_KEY,
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_KEY
            )
            uninstall_files.append(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_KEY
            )

        if self._need_ca_cert:
            self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
                filetransaction.FileTransaction(
                    name=(
                        ogdwhcons.FileLocations.
                        OVIRT_ENGINE_PKI_GRAFANA_APACHE_CA_CERT
                    ),
                    mode=0o644,
                    owner=self.environment[oengcommcons.SystemEnv.USER_ROOT],
                    enforcePermissions=True,
                    content=self._apache_ca_cert,
                    binary=True,
                    modifiedList=uninstall_files,
                )
            )
            if not os.path.lexists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
            ):
                os.symlink(
                    ogdwhcons.FileLocations.
                    OVIRT_ENGINE_PKI_GRAFANA_APACHE_CA_CERT,
                    oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
                )
                uninstall_files.append(
                    oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
                )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLEANUP,
        condition=lambda self: (
            self._enabled
        ),
    )
    def _cleanup(self):
        self._enrolldata.cleanup()


# vim: expandtab tabstop=4 shiftwidth=4
