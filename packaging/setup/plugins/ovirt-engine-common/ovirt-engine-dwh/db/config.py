#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Config plugin."""


import os
import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Config plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.ConfigEnv.OVIRT_ENGINE_DWH_DB_BACKUP_DIR,
            odwhcons.FileLocations.OVIRT_ENGINE_DEFAULT_DWH_DB_BACKUP_DIR
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
    )
    def _validation(self):
        path = self.environment[
            odwhcons.ConfigEnv.OVIRT_ENGINE_DWH_DB_BACKUP_DIR
        ]
        if not os.path.exists(path):
            raise RuntimeError(
                _(
                    'Backup path {path} not found'
                ).format(
                    path=path,
                )
            )


# vim: expandtab tabstop=4 shiftwidth=4
