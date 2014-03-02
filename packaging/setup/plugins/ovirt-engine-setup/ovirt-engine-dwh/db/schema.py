#
# ovirt-engine-setup -- ovirt engine setup
# Copyright (C) 2013 Red Hat, Inc.
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
from ovirt_engine_setup import dwhconstants as odwhcons
from ovirt_engine_setup import database


@util.export
class Plugin(plugin.PluginBase):
    """Schema plugin."""

    class SchemaTransaction(transaction.TransactionElement):
        """yum transaction element."""

        def __init__(self, parent, backup=None):
            self._parent = parent
            self._backup = backup

        def __str__(self):
            return _("DWH schema Transaction")

        def prepare(self):
            pass

        def abort(self):
            self._parent.logger.info(_('Rolling back DWH database schema'))
            try:
                dbovirtutils = database.OvirtUtils(
                    plugin=self._parent,
                    dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
                )
                self._parent.logger.info(
                    _('Clearing DWH database {database}').format(
                        database=self._parent.environment[
                            odwhcons.DBEnv.DATABASE
                        ],
                    )
                )
                dbovirtutils.clearDatabase()
                if self._backup is not None and os.path.exists(self._backup):
                    self._parent.logger.info(
                        _('Restoring DWH database {database}').format(
                            database=self._parent.environment[
                                odwhcons.DBEnv.DATABASE
                            ],
                        )
                    )
                    dbovirtutils.restore(backupFile=self._backup)
            except Exception as e:
                self._parent.logger.debug(
                    'Exception during DWH database restore',
                    exc_info=True,
                )
                self._parent.logger.error(
                    _('DWH database rollback failed: {error}').format(
                        error=e,
                    )
                )

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
                    'Please execute: {command}\n'
                    'Using the password of the "postgres" user.'
                ).format(
                    command=(
                        '{cmd} '
                        '-s {server} '
                        '-p {port} '
                        '-d {db} '
                        '-f postgres '
                        '-t {user}'
                    ).format(
                        cmd=(
                            osetupcons.FileLocations.
                            OVIRT_ENGINE_DB_CHANGE_OWNER
                        ),
                        server=self.environment[odwhcons.DBEnv.HOST],
                        port=self.environment[odwhcons.DBEnv.PORT],
                        db=self.environment[odwhcons.DBEnv.DATABASE],
                        user=self.environment[odwhcons.DBEnv.USER],
                    ),
                )
            )

    @plugin.event(
        stage=plugin.Stages.STAGE_VALIDATION,
        after=(
            odwhcons.Stages.DB_CREDENTIALS_AVAILABLE,
        ),
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
        backupFile = None

        if not self.environment[
            odwhcons.DBEnv.NEW_DATABASE
        ]:
            dbovirtutils = database.OvirtUtils(
                plugin=self,
                dbenvkeys=odwhcons.Const.DWH_DB_ENV_KEYS,
            )
            backupFile = dbovirtutils.backup(
                dir=odwhcons.FileLocations.OVIRT_ENGINE_DWH_DB_BACKUP_DIR,
                prefix=odwhcons.Const.OVIRT_ENGINE_DWH_DB_BACKUP_PREFIX,
            )

        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            self.SchemaTransaction(
                parent=self,
                backup=backupFile,
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
                osetupcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR
            ):
                os.makedirs(
                    osetupcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR
                )
            args.extend(
                [
                    '-m',
                    os.path.join(
                        osetupcons.FileLocations.OVIRT_ENGINE_DB_MD5_DIR,
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


# vim: expandtab tabstop=4 shiftwidth=4
