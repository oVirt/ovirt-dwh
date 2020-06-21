#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""grafana database plugins."""


from otopi import util

from . import dwh_connection


@util.export
def createPlugins(context):
    dwh_connection.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
