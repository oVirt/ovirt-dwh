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
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


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
            oengcommcons.Stages.DIALOG_TITLES_E_PKI,
        ),
        after=(
            ogdwhcons.Stages.CORE_ENABLE,
            oenginecons.Stages.CORE_ENABLE,
            oengcommcons.Stages.DIALOG_TITLES_S_PKI,
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
    def _customization(self):
        engine_apache_pki_found = (
            os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_KEY
            ) and os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CA_CERT
            ) and os.path.exists(
                oengcommcons.FileLocations.OVIRT_ENGINE_PKI_APACHE_CERT
            )
        )

        if not engine_apache_pki_found:
            self._enabled = True
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
