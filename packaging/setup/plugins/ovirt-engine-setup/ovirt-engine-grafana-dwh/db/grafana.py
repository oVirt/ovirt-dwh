#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""internal grafana database plugin."""


import gettext
import os

from otopi import plugin
from otopi import util

from ovirt_engine_setup import util as osetuputil
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """internal grafana database plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._db = os.path.join(
            ogdwhcons.FileLocations.GRAFANA_STATE_DIR,
            ogdwhcons.FileLocations.GRAFANA_DB
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.NEW_DATABASE,
            True
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
    )
    def _setup_check_new_database(self):
        if os.path.exists(self._db) and os.stat(self._db).st_size > 0:
            self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE] = False

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self.environment[ogdwhcons.CoreEnv.ENABLE] and
            self.environment[ogdwhcons.ConfigEnv.NEW_DATABASE]
        ),
    )
    def _misc_set_access(self):
        # TODO: Perhaps do this conditionally, only if needed
        with open(self._db, 'a'):
            pass
        os.chmod(
            ogdwhcons.FileLocations.GRAFANA_STATE_DIR,
            0o750
        )
        os.chmod(
            self._db,
            0o640
        )
        for obj in (
            ogdwhcons.FileLocations.GRAFANA_STATE_DIR,
            self._db,
        ):
            os.chown(
                obj,
                osetuputil.getUid(
                    self.environment[ogdwhcons.ConfigEnv.GRAFANA_USER]
                ),
                osetuputil.getGid(
                    self.environment[ogdwhcons.ConfigEnv.GRAFANA_GROUP]
                )
            )
        self.environment[ogdwhcons.ConfigEnv.GRAFANA_DB_CREATED_BY_US] = True

# vim: expandtab tabstop=4 shiftwidth=4
