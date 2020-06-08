#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import grafana_db
from . import service


@util.export
def createPlugins(context):
    grafana_db.Plugin(context=context)
    service.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
