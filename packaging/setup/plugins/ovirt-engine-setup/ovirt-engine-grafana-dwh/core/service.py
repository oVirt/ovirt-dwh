#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


import gettext
import os


from otopi import util
from otopi import plugin
from otopi import filetransaction
from otopi import transaction


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.grafana_dwh import constants as ogdwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):

    class SystemdTempConfTransaction(transaction.TransactionElement):
        """systemd temporary conf transaction element."""

        def __init__(self, parent, service, values):
            self._parent = parent
            self._service = service
            self._values = values
            self._dir = os.path.join(
                '/etc',
                'systemd',
                'system',
                '{}.service.d'.format(service),
            )
            self._conf = os.path.join(
                self._dir,
                'engine-setup-temporary.conf',
            )
            self._direxisted = False
            self._conftransaction = transaction.Transaction()

        def __str__(self):
            return _("systemd temporary conf Transaction")

        def _reload_systemd_conf(self):
            systemctl = self._parent.command.get('systemctl', optional=True)
            if systemctl is not None:
                self._parent.execute(
                    args=(
                        systemctl,
                        'daemon-reload',
                    ),
                    raiseOnError=False,
                )

        def prepare(self):
            self._direxisted = os.path.exists(self._dir)
            if not self._direxisted:
                os.makedirs(self._dir)
            content = [
                '[Service]',
            ] + [
                '{k}={v}'.format(k=k, v=val)
                for k, val in self._values.items()
            ]
            self._conftransaction.append(
                filetransaction.FileTransaction(
                    name=self._conf,
                    content=content,
                    visibleButUnsafe=True,
                )
            )
            self._conftransaction.prepare()
            self._reload_systemd_conf()

        def abort(self):
            self._conftransaction.abort()
            if not self._direxisted:
                os.rmdir(self._dir)
            self._reload_systemd_conf()

        def commit(self):
            self._conftransaction.commit()

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            ogdwhcons.ConfigEnv.GRAFANA_PORT,
            ogdwhcons.Defaults.GRAFANA_PORT
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: (
            not self.environment[
                osetupcons.CoreEnv.DEVELOPER_MODE
            ] and
            self.environment[
                ogdwhcons.CoreEnv.ENABLE
            ]
        ),
    )
    def _closeup_grafana_service(self):
        self.logger.info(_('Starting Grafana service'))
        # If this is initial setup, grafana startup does also provisioning.
        # This can take a rather long time on slow/loaded machines.
        # systemd's default DefaultTimeoutStartSec is 90 seconds.
        # Temporarily allow grafana more time.
        localtransaction = transaction.Transaction()
        try:
            localtransaction.append(
                self.SystemdTempConfTransaction(
                    parent=self,
                    service=ogdwhcons.Const.SERVICE_NAME,
                    values={
                        'TimeoutStartSec': '300',
                    },
                )
            )
            localtransaction.prepare()
            self.services.state(
                name=ogdwhcons.Const.SERVICE_NAME,
                state=True,
            )
        finally:
            localtransaction.abort()

        self.services.startup(
            name=ogdwhcons.Const.SERVICE_NAME,
            state=True,
        )


# vim: expandtab tabstop=4 shiftwidth=4
