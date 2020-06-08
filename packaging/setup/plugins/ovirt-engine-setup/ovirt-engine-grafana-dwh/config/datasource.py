#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext


from otopi import constants as otopicons
from otopi import filetransaction
from otopi import util
from otopi import plugin

from ovirt_engine import util as outil

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self.environment[ogdwhcons.CoreEnv.ENABLE],
    )
    def _misc_grafana_datasource_config(self):
        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_grafana_files',
            fileList=uninstall_files,
        )
        substs = {}
        for e, k in (
            (odwhcons.DBEnv.HOST, 'GRAFANA_DB_HOST'),
            (odwhcons.DBEnv.PORT, 'GRAFANA_DB_PORT'),
            (ogdwhcons.GrafanaDBEnv.USER, 'GRAFANA_DB_USER'),
            (ogdwhcons.GrafanaDBEnv.PASSWORD, 'GRAFANA_DB_PASSWORD'),
            (odwhcons.DBEnv.DATABASE, 'GRAFANA_DB_DATABASE'),
        ):
            substs['@{}@'.format(k)] = self.environment[e]
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    ogdwhcons.FileLocations.
                    GRAFANA_PROVISIONING_DWH_DATASOURCE
                ),
                mode=0o640,
                owner='root',
                group='grafana',
                enforcePermissions=True,
                content=outil.processTemplate(
                    template=(
                        ogdwhcons.FileLocations.
                        GRAFANA_PROVISIONING_DWH_DATASOURCE_TEMPLATE
                    ),
                    subst=substs,
                ),
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
