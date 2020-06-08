#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import check_etl
from . import single_etl
from . import config
from . import misc
from . import remote_engine
from . import scale
from . import service
from . import dwh
from . import dwh_database


@util.export
def createPlugins(context):
    check_etl.Plugin(context=context)
    single_etl.Plugin(context=context)
    config.Plugin(context=context)
    misc.Plugin(context=context)
    remote_engine.Plugin(context=context)
    scale.Plugin(context=context)
    service.Plugin(context=context)
    dwh.Plugin(context=context)
    dwh_database.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
