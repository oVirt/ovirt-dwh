#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext
import rpm

from otopi import util
from otopi import plugin

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import util as osetuputil


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """
    This plugin is for configuring selinux for grafana package.
    Grafana package from the version 9.2.10-10 has subpackage with selinux configurations.
    And with initial configurations grafana can't communicate with postgresql.
    From the version 9.2.10-15 there is the flag to control possibility for grafana to query local postgresql.
    In this plugin we check grafana package version and enable selinux flag for postgresql if needed.
    """

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._should_enable_selinux_bool = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION
    )
    def _misc_check_grafana_version_for_selinux(self):
        _, mini_pm, _ = (osetuputil.getPackageManager(self.logger))
        queried_packages = mini_pm().queryPackages(patterns=['grafana'])

        grafana_pkg_info = next(
            (package for package in queried_packages if package['operation'] == 'installed' and package['name'] == 'grafana'),
            None
        )
        if grafana_pkg_info:
            version = grafana_pkg_info['version']  # looks like '9.2.10'
            release = grafana_pkg_info['release']  # looks like '15.el8'
            patch = release.split('.')[0]  # remove part with OS stream

            # We are on the version without selinux configured, can do nothing with selinux.
            if rpm.labelCompare(('1', version, patch), ('1', '9.2.10', '10')) < 0:
                self._should_enable_selinux_bool = False
                return

            # We are on the version with selinux flag added, should enable it.
            if rpm.labelCompare(('1', version, patch), ('1', '9.2.10', '15')) >= 0:
                self._should_enable_selinux_bool = True
                return

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        before=(
                osetupcons.Stages.SETUP_SELINUX,
        ),
        condition=lambda self: self._should_enable_selinux_bool,
    )
    def _misc_selinux_allow_grafana_request_postgresql(self):
        self.environment[osetupcons.SystemEnv.SELINUX_BOOLEANS].append({
            'boolean': 'grafana_can_tcp_connect_postgresql_port',
            'state': "on",
        })

# vim: expandtab tabstop=4 shiftwidth=4
