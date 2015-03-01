#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013-2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Schema plugin."""


import os
import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-dwh')


from otopi import constants as otopicons
from otopi import util
from otopi import plugin
from otopi import transaction


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup import dialog
from ovirt_engine_setup.engine_common \
    import constants as oengcommcons


@util.export
class Plugin(plugin.PluginBase):
    """Schema plugin."""

    class SchemaTransaction(transaction.TransactionElement):
        """yum transaction element."""

        def __init__(self, parent):
            self._parent = parent

        def __str__(self):
            return _("DWH schema Transaction")

        def prepare(self):
            pass

        def abort(self):
            if (
                self._parent.environment[
                    odwhcons.DBEnv.RESTORE_BACKUP_LATE
                ] and
                self._parent._backup
            ):
                self._parent._needRollback = True
                self._parent.logger.warning(
                    _('Rollback of DWH database postponed to Stage "Clean up"')
                )
            else:
                self._parent.logger.info(_('Rolling back DWH database schema'))
                self._parent._rollbackDatabase()

        def commit(self):
            pass

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    def _checkDatabaseOwnership(self):
        statement = database.Statement(
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            environment=self.environment,
        )
        result = statement.execute(
            statement="""
                select
                    nsp.nspname as object_schema,
                    cls.relname as object_name,
                    rol.rolname as owner,
                    case cls.relkind
                        when 'r' then 'TABLE'
                        when 'i' then 'INDEX'
                        when 'S' then 'SEQUENCE'
                        when 'v' then 'VIEW'
                        when 'c' then 'TYPE'
                    else
                        cls.relkind::text
                    end as object_type
                from
                    pg_class cls join
                    pg_roles rol on rol.oid = cls.relowner join
                    pg_namespace nsp on nsp.oid = cls.relnamespace
                where
                    nsp.nspname not in ('information_schema', 'pg_catalog') and
                    nsp.nspname not like 'pg_%%' and
                    rol.rolname != %(user)s
                order by
                    nsp.nspname,
                    cls.relname
            """,
            args=dict(
                user=self.environment[odwhcons.DBEnv.USER],
            ),
            ownConnection=True,
            transaction=False,
        )
        if len(result) > 0:
            raise RuntimeError(
                _(
                    'Cannot upgrade the DWH database schema due to wrong '
                    'ownership of some database entities.\n'
                )
            )

    def _rollbackDatabase(self):
        try:
            dbovirtutils = database.OvirtUtils(
                plugin=self,
                dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            )
            self.logger.info(
                _('Clearing DWH database {database}').format(
                    database=self.environment[
                        odwhcons.DBEnv.DATABASE
                    ],
                )
            )
            dbovirtutils.clearDatabase()
            if self._backup is not None and os.path.exists(self._backup):
                self.logger.info(
                    _('Restoring DWH database {database}').format(
                        database=self.environment[
                            odwhcons.DBEnv.DATABASE
                        ],
                    )
                )
                dbovirtutils.restore(backupFile=self._backup)
        except Exception as e:
            self.logger.debug(
                'Exception during DWH database restore',
                exc_info=True,
            )
            self.logger.error(
                _('DWH database rollback failed: {error}').format(
                    error=e,
                )
            )

    def _getDBSize(self):
        # Returns db size in bytes
        statement = database.Statement(
            dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            environment=self.environment,
        )
        result = statement.execute(
            statement="SELECT pg_database_size(%(db)s) as size",
            args=dict(
                db=self.environment[odwhcons.DBEnv.DATABASE],
            ),
            ownConnection=True,
            transaction=False,
        )
        return int(result[0]['size'])

    def _HumanReadableSize(self, bytes):
        size_in_mb = bytes / pow(2, 20)
        return (
            _('{size} MB').format(size=size_in_mb)
            if size_in_mb < 1024
            else _('{size:1.1f} GB').format(
                size=size_in_mb/1024.0,
            )
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
    )
    def _init(self):
        self.environment.setdefault(
            odwhcons.DBEnv.PERFORM_BACKUP,
            None
        )
        self.environment.setdefault(
            odwhcons.DBEnv.RESTORE_BACKUP_LATE,
            True
        )
        self._needRollback = False

    @plugin.event(
        stage=plugin.Stages.STAGE_CUSTOMIZATION,
        condition=lambda self: not self.environment[
            odwhcons.DBEnv.NEW_DATABASE
        ],
        before=(
            oengcommcons.Stages.DIALOG_TITLES_E_DATABASE,
        ),
        after=(
            odwhcons.Stages.DB_CONNECTION_CUSTOMIZATION,
        ),
    )
    def _customization(self):
        if self.environment[odwhcons.DBEnv.PERFORM_BACKUP] is None:
            perform_backup = dialog.queryBoolean(
                dialog=self.dialog,
                name='OVESETUP_DWH_PERFORM_BACKUP',
                note=_(
                    'The detected DWH database size is {dbsize}.\n'
                    'Setup can backup the existing database. The time and '
                    'space required for the database backup depend on its '
                    'size. This process '
                    'takes time, and in some cases (for instance, when the '
                    'size is few GBs) may take several hours to complete.\n'
                    'If you choose to not back up the database, and Setup '
                    'later fails for some reason, it will not be able to '
                    'restore the database and all DWH data will be lost.\n'
                    'Would you like to backup the existing database before '
                    'upgrading it? '
                    '(@VALUES@) [@DEFAULT@]: '
                ).format(
                    dbsize=self._HumanReadableSize(self._getDBSize()),
                ),
                prompt=True,
                true=_('Yes'),
                false=_('No'),
                default=True,
            )
            if not perform_backup:
                self.logger.warning(
                    _(
                        'Are you sure you do not want to backup the DWH '
                        'database?'
                    )
                )
                perform_backup = not dialog.queryBoolean(
                    dialog=self.dialog,
                    name='OVESETUP_DWH_VERIFY_NO_BACKUP',
                    note=_(
                        'A positive reply makes sense only if '
                        'you do not need the data in DWH, or have some other, '
                        'external means to restore it to a working state.\n'
                        'Are you sure you do not want to backup the DWH '
                        'database?'
                        '(@VALUES@) [@DEFAULT@]: '
                    ).format(
                        dbsize=self._HumanReadableSize(self._getDBSize()),
                    ),
                    prompt=True,
                    true=_('Yes'),
                    false=_('No'),
                    default=False,
                )
                if perform_backup:
                    self.dialog.note(
                        text=_(
                            'The DWH Database will be backed up prior '
                            'to upgrade.'
                        ),
                    )
            if not perform_backup:
                self.logger.warning(
                    _(
                        'DWH Database will not be backed up. Rollback in case '
                        'of failure will not be possible.'
                    )
                )
            self.environment[
                odwhcons.DBEnv.PERFORM_BACKUP
            ] = perform_backup

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        condition=lambda self: (
            self.environment[odwhcons.CoreEnv.ENABLE] and
            not self.environment[
                odwhcons.DBEnv.NEW_DATABASE
            ]
        ),
    )
    def _validation(self):
        self._checkDatabaseOwnership()

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=odwhcons.Stages.DB_SCHEMA,
        condition=lambda self: self.environment[
            odwhcons.CoreEnv.ENABLE
        ],
        after=(
            odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
        ),
    )
    def _misc(self):
        self._backup = None

        if not self.environment[
            odwhcons.DBEnv.NEW_DATABASE
        ] and self.environment[
            odwhcons.DBEnv.PERFORM_BACKUP
        ]:
            dbovirtutils = database.OvirtUtils(
                plugin=self,
                dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            )
            self._backup = dbovirtutils.backup(
                dir=self.environment[
                    odwhcons.ConfigEnv.OVIRT_ENGINE_DWH_DB_BACKUP_DIR
                ],
                prefix=odwhcons.Const.OVIRT_ENGINE_DWH_DB_BACKUP_PREFIX,
            )

        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            self.SchemaTransaction(
                parent=self,
            )
        )

        self.logger.info(_('Creating/refreshing DWH database schema'))
        args = [
            odwhcons.FileLocations.OVIRT_ENGINE_DWH_DB_SCHMA_TOOL,
            '-s', self.environment[odwhcons.DBEnv.HOST],
            '-p', str(self.environment[odwhcons.DBEnv.PORT]),
            '-u', self.environment[odwhcons.DBEnv.USER],
            '-d', self.environment[odwhcons.DBEnv.DATABASE],
            '-l', self.environment[otopicons.CoreEnv.LOG_FILE_NAME],
            '-c', 'apply',
        ]
        if self.environment[
            osetupcons.CoreEnv.DEVELOPER_MODE
        ]:
            if not os.path.exists(
                odwhcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR
            ):
                os.makedirs(
                    odwhcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR
                )
            args.extend(
                [
                    '-m',
                    os.path.join(
                        odwhcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR,
                        '%s-%s.scripts.md5' % (
                            self.environment[odwhcons.DBEnv.HOST],
                            self.environment[odwhcons.DBEnv.DATABASE],
                        ),
                    ),
                ]
            )
        self.execute(
            args=args,
            envAppend={
                'DBFUNC_DB_PGPASSFILE': self.environment[
                    odwhcons.DBEnv.PGPASS_FILE
                ]
            },
        )

    @plugin.event(
        stage=plugin.Stages.STAGE_CLEANUP,
        priority=plugin.Stages.PRIORITY_LAST,
        condition=lambda self: self._needRollback,
    )
    def _rollback(self):
        self.logger.warning(
            _('Rollback of DWH database started')
        )
        self.dialog.note(
            text=_(
                'This might be a long process, but it should be safe to '
                'start the engine service before it finishes, if needed.'
            ),
        )
        self._rollbackDatabase()


# vim: expandtab tabstop=4 shiftwidth=4
