#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""ovirt-engine-setup dwh grafana integration core plugin."""


from otopi import util


from . import misc
from . import service


@util.export
def createPlugins(context):
    misc.Plugin(context=context)
    service.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
