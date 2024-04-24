#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""ovirt-engine-setup grafana config plugin."""


from otopi import util

from . import database
from . import datasource
from . import selinux


@util.export
def createPlugins(context):
    database.Plugin(context=context)
    datasource.Plugin(context=context)
    selinux.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
