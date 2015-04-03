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


"""Database plugin."""


import gettext


from otopi import constants as otopicons
from otopi import util
from otopi import filetransaction
from otopi import plugin


from ovirt_engine import util as outil


from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.dwh import constants as odwhcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


@util.export
class Plugin(plugin.PluginBase):
    """Databsae plugin."""

    def _getDBConfig(
        self,
        prefix,
        host,
        port,
        user,
        password,
        database,
        secured,
        hostValidation,
    ):
        return (
            '{prefix}_DB_HOST="{host}"\n'
            '{prefix}_DB_PORT="{port}"\n'
            '{prefix}_DB_USER="{user}"\n'
            '{prefix}_DB_PASSWORD="{password}"\n'
            '{prefix}_DB_DATABASE="{database}"\n'
            '{prefix}_DB_SECURED="{secured}"\n'
            '{prefix}_DB_SECURED_VALIDATION="{hostValidation}"\n'
            '{prefix}_DB_DRIVER="org.postgresql.Driver"\n'
            '{prefix}_DB_URL=' + (
                '"'
                'jdbc:postgresql://'
                '${{{prefix}_DB_HOST}}:${{{prefix}_DB_PORT}}'
                '/${{{prefix}_DB_DATABASE}}'
                '?{jdbcTlsOptions}'
                '"\n'
            ) +
            ''
        ).format(
            prefix=prefix,
            host=host,
            port=port,
            user=user,
            password=outil.escape(
                password,
                '"\\$',
            ),
            database=database,
            secured=secured,
            hostValidation=hostValidation,
            jdbcTlsOptions='&'.join(
                s for s in (
                    'ssl=true' if secured else '',
                    (
                        'sslfactory='
                        'org.postgresql.ssl.NonValidatingFactory'
                    ) if not hostValidation else ''
                ) if s
            ),
        )

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self.environment[odwhcons.CoreEnv.ENABLE],
    )
    def _misc(self):
        uninstall_files = []
        self.environment[
            osetupcons.CoreEnv.REGISTER_UNINSTALL_GROUPS
        ].addFiles(
            group='ovirt_dwh_files',
            fileList=uninstall_files,
        )
        self.environment[otopicons.CoreEnv.MAIN_TRANSACTION].append(
            filetransaction.FileTransaction(
                name=(
                    odwhcons.FileLocations.
                    OVIRT_ENGINE_DWHD_SERVICE_CONFIG_DATABASE
                ),
                mode=0o600,
                owner=self.environment[osetupcons.SystemEnv.USER_ENGINE],
                enforcePermissions=True,
                content='%s%s' % (
                    self._getDBConfig(
                        prefix='ENGINE',
                        host=self.environment[
                            odwhcons.EngineDBEnv.HOST
                        ],
                        port=self.environment[
                            odwhcons.EngineDBEnv.PORT
                        ],
                        user=self.environment[
                            odwhcons.EngineDBEnv.USER
                        ],
                        password=self.environment[
                            odwhcons.EngineDBEnv.PASSWORD
                        ],
                        database=self.environment[
                            odwhcons.EngineDBEnv.DATABASE
                        ],
                        secured=self.environment[
                            odwhcons.EngineDBEnv.SECURED
                        ],
                        hostValidation=self.environment[
                            odwhcons.EngineDBEnv.SECURED_HOST_VALIDATION
                        ],
                    ),
                    self._getDBConfig(
                        prefix='DWH',
                        host=self.environment[odwhcons.DBEnv.HOST],
                        port=self.environment[odwhcons.DBEnv.PORT],
                        user=self.environment[odwhcons.DBEnv.USER],
                        password=self.environment[odwhcons.DBEnv.PASSWORD],
                        database=self.environment[odwhcons.DBEnv.DATABASE],
                        secured=self.environment[odwhcons.DBEnv.SECURED],
                        hostValidation=self.environment[
                            odwhcons.DBEnv.SECURED_HOST_VALIDATION
                        ],
                    ),
                ),
                modifiedList=uninstall_files,
            )
        )


# vim: expandtab tabstop=4 shiftwidth=4
