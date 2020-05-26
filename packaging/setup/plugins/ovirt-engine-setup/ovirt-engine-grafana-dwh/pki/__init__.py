#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import apache
from . import misc


@util.export
def createPlugins(context):
    apache.Plugin(context=context)
    misc.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
