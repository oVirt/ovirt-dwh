#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import connection
from . import engine_connection
from . import dbmsupgrade
from . import schema
from . import vacuum
from . import engine_fqdn


@util.export
def createPlugins(context):
    connection.Plugin(context=context)
    engine_connection.Plugin(context=context)
    dbmsupgrade.Plugin(context=context)
    schema.Plugin(context=context)
    vacuum.Plugin(context=context)
    engine_fqdn.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
