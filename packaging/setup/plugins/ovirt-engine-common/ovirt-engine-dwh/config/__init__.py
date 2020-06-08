#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


from otopi import util


from . import dwh_uuid


@util.export
def createPlugins(context):
    dwh_uuid.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
