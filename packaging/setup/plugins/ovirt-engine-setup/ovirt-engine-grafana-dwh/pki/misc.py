#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""misc PKI plugin."""


import gettext
import os

from otopi import plugin
from otopi import util

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import util as osetuputil
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """misc pki plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    def _install_d(self, dirname, mode=None, uid=-1, gid=-1):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            if mode is not None:
                os.chmod(dirname, mode)
            os.chown(dirname, uid, gid)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.KEY_SIZE,
            ogdwhcons.Defaults.DEFAULT_KEY_SIZE
        )
        self._enabled = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
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
    def _customization(self):
        self._enabled = True

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=ogdwhcons.Stages.PKI_MISC,
        condition=lambda self: (
            self._enabled
        ),
        after=(
            oenginecons.Stages.CA_AVAILABLE,
        ),
    )
    def _misc_pki(self):
        ovirtuid = osetuputil.getUid(
            self.environment[osetupcons.SystemEnv.USER_ENGINE]
        )
        ovirtgid = osetuputil.getGid(
            self.environment[osetupcons.SystemEnv.GROUP_ENGINE]
        )
        rootuid = osetuputil.getGid(
            self.environment[oengcommcons.SystemEnv.USER_ROOT]
        )
        self._install_d(
            dirname=oenginecons.FileLocations.OVIRT_ENGINE_PKIDIR,
            mode=0o755,
            uid=ovirtuid,
            gid=ovirtgid,
        )
        self._install_d(
            dirname=oenginecons.FileLocations.OVIRT_ENGINE_PKIKEYSDIR,
            mode=0o755,
            uid=rootuid,
            gid=-1,
        )
        self._install_d(
            dirname=oenginecons.FileLocations.OVIRT_ENGINE_PKICERTSDIR,
            mode=0o755,
            uid=ovirtuid,
            gid=ovirtgid,
        )


# vim: expandtab tabstop=4 shiftwidth=4
