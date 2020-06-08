#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import clear
from . import single_etl


@util.export
def createPlugins(context):
    clear.Plugin(context=context)
    single_etl.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
