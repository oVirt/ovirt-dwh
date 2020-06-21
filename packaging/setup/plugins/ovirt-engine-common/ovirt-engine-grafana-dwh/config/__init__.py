#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""ovirt-engine-setup grafana config plugin."""


from otopi import util

from . import grafana_fqdn


@util.export
def createPlugins(context):
    grafana_fqdn.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
