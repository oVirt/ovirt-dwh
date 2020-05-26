#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import config
from . import misc
from . import remote_engine
from . import service


@util.export
def createPlugins(context):
    config.Plugin(context=context)
    misc.Plugin(context=context)
    remote_engine.Plugin(context=context)
    service.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
