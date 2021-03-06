#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""oVirt engine-setup dwh grafana datebase plugin."""


from otopi import util

from . import connection
from . import grafana


@util.export
def createPlugins(context):
    connection.Plugin(context=context)
    grafana.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
