#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Clear plugin."""


import gettext


from otopi import util
from otopi import plugin


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_setup_lib import dialog


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Clear plugin."""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.RemoveEnv.REMOVE_DATABASE,
            None
        )
        self._bkpfile = None

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        after=(
            osetupcons.Stages.REMOVE_CUSTOMIZATION_COMMON,
        ),
    )
    def _customization(self):
        if self.environment[
            osetupcons.RemoveEnv.REMOVE_ALL
        ]:
            self.environment[
                odwhcons.RemoveEnv.REMOVE_DATABASE
            ] = True

        if self.environment[
            odwhcons.RemoveEnv.REMOVE_DATABASE
        ] is None:
            self.environment[
                odwhcons.RemoveEnv.REMOVE_DATABASE
            ] = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_DWH_REMOVE_DATABASE',
                note=_(
                    'Do you want to remove DWH DB content? All data will '
                    'be lost (@VALUES@) [@DEFAULT@]: '
                ),
                prompt=True,
                true=_('Yes'),
                false=_('No'),
                default=False,
            )
        if self.environment[odwhcons.RemoveEnv.REMOVE_DATABASE]:
            self.environment[odwhcons.ConfigEnv.DWH_SERVICE_STOP_NEEDED] = True

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: (
            self.environment[odwhcons.DBEnv.PASSWORD] is not None and
            self.environment[odwhcons.RemoveEnv.REMOVE_DATABASE]
        ),
        after=(
            odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
        ),
    )
    def _misc(self):

        try:
            dbovirtutils = database.OvirtUtils(
                plugin=self,
                dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            )
            dbovirtutils.tryDatabaseConnect()
            self._bkpfile = dbovirtutils.backup(
                dir=self.environment[
                    odwhcons.ConfigEnv.OVIRT_ENGINE_DWH_DB_BACKUP_DIR
                ],
                prefix=odwhcons.Const.OVIRT_ENGINE_DWH_DB_BACKUP_PREFIX,
            )
            self.logger.info(
                _('Clearing DWH database {database}').format(
                    database=self.environment[odwhcons.DBEnv.DATABASE],
                )
            )
            dbovirtutils.clearDatabase()

        except RuntimeError as e:
            self.logger.debug('exception', exc_info=True)
            self.logger.warning(
                _(
                    'Cannot clear DWH database: {error}'
                ).format(
                    error=e,
                )
            )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLOSEUP,
        condition=lambda self: self._bkpfile is not None,
        before=(
            osetupcons.Stages.DIALOG_TITLES_E_SUMMARY,
        ),
        after=(
            osetupcons.Stages.DIALOG_TITLES_S_SUMMARY,
        ),
    )
    def _closeup(self):
        self.dialog.note(
            text=_(
                'A backup of the DWH database is available at {path}'
            ).format(
                path=self._bkpfile
            ),
        )

# vim: expandtab tabstop=4 shiftwidth=4
