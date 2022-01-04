#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#


"""Grafana DWH Constants."""


import os
import gettext


from otopi import util

from ovirt_engine_setup.constants import classproperty
from ovirt_engine_setup.constants import osetupattrsclass
from ovirt_engine_setup.constants import osetupattrs
from ovirt_engine_setup.dwh import constants as odwhcons
from ovirt_engine_setup.dwh.constants import DBEnv as DWHDBEnv
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons


from . import config


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-dwh')


DEK = oengcommcons.DBEnvKeysConst


@util.export
@util.codegen
class Const(object):
    SERVICE_NAME = 'grafana-server'
    OVIRT_ENGINE_GRAFANA_DWH_SETUP_PACKAGE_NAME = \
        'ovirt-engine-dwh-grafana-integration-setup'
    GRAFANA_URI_PATH = '/ovirt-engine-grafana'

    @classproperty
    def DWH_DB_ENV_KEYS(self):
        return {
            DEK.HOST: DWHDBEnv.HOST,
            DEK.PORT: DWHDBEnv.PORT,
            DEK.SECURED: DWHDBEnv.SECURED,
            DEK.HOST_VALIDATION: DWHDBEnv.SECURED_HOST_VALIDATION,
            DEK.USER: DWHDBEnv.USER,
            DEK.PASSWORD: DWHDBEnv.PASSWORD,
            DEK.DATABASE: DWHDBEnv.DATABASE,
            DEK.CONNECTION: DWHDBEnv.CONNECTION,
            DEK.PGPASSFILE: DWHDBEnv.PGPASS_FILE,
            DEK.NEW_DATABASE: DWHDBEnv.NEW_DATABASE,
            DEK.NEED_DBMSUPGRADE: DWHDBEnv.NEED_DBMSUPGRADE,
            DEK.DUMPER: DWHDBEnv.DUMPER,
            DEK.FILTER: DWHDBEnv.FILTER,
            DEK.RESTORE_JOBS: DWHDBEnv.RESTORE_JOBS,
        }

    @classproperty
    def DEFAULT_DWH_DB_ENV_KEYS(self):
        return {
            DEK.HOST: DWHDefaults.DEFAULT_DB_HOST,
            DEK.PORT: DWHDefaults.DEFAULT_DB_PORT,
            DEK.SECURED: DWHDefaults.DEFAULT_DB_SECURED,
            DEK.HOST_VALIDATION:
                DWHDefaults.DEFAULT_DB_SECURED_HOST_VALIDATION,
            DEK.USER: DWHDefaults.DEFAULT_DB_USER,
            DEK.PASSWORD: DWHDefaults.DEFAULT_DB_PASSWORD,
            DEK.DATABASE: DWHDefaults.DEFAULT_DB_DATABASE,
        }

    @classproperty
    def GRAFANA_DB_ENV_KEYS(self):
        return {
            DEK.HOST: DWHDBEnv.HOST,
            DEK.PORT: DWHDBEnv.PORT,
            DEK.SECURED: DWHDBEnv.SECURED,
            DEK.HOST_VALIDATION: DWHDBEnv.SECURED_HOST_VALIDATION,
            DEK.USER: GrafanaDBEnv.USER,
            DEK.PASSWORD: GrafanaDBEnv.PASSWORD,
            DEK.DATABASE: DWHDBEnv.DATABASE,
            DEK.CONNECTION: DWHDBEnv.CONNECTION,
            DEK.PGPASSFILE: DWHDBEnv.PGPASS_FILE,
            DEK.NEW_DATABASE: DWHDBEnv.NEW_DATABASE,
            DEK.NEED_DBMSUPGRADE: DWHDBEnv.NEED_DBMSUPGRADE,
            DEK.DUMPER: DWHDBEnv.DUMPER,
            DEK.FILTER: DWHDBEnv.FILTER,
            DEK.RESTORE_JOBS: DWHDBEnv.RESTORE_JOBS,
        }

    @classproperty
    def DEFAULT_GRAFANA_DB_ENV_KEYS(self):
        return {
            DEK.HOST: DWHDefaults.DEFAULT_DB_HOST,
            DEK.PORT: DWHDefaults.DEFAULT_DB_PORT,
            DEK.SECURED: DWHDefaults.DEFAULT_DB_SECURED,
            DEK.HOST_VALIDATION:
                DWHDefaults.DEFAULT_DB_SECURED_HOST_VALIDATION,
            DEK.USER: GrafanaDefaults.DEFAULT_DB_USER,
            DEK.PASSWORD: GrafanaDefaults.DEFAULT_DB_PASSWORD,
            DEK.DATABASE: DWHDefaults.DEFAULT_DB_DATABASE,
        }

    # Is there a need to make this configurable?
    OVIRT_GRAFANA_SSO_CLIENT_ID = 'ovirt-grafana'

    PKI_GRAFANA_APACHE_CERT_NAME = 'apache-grafana'


@util.export
@util.codegen
class Defaults(object):
    DEFAULT_ADDITIONAL_PACKAGES = (
        'grafana'
        ',grafana-postgres'
    )
    GRAFANA_PORT = 3000
    GRAFANA_DEFAULT_USER = 'grafana'
    GRAFANA_DEFAULT_GROUP = 'grafana'
    DEFAULT_KEY_SIZE = 2048


@util.export
@util.codegen
class DWHDefaults(object):
    DEFAULT_DB_HOST = ''
    DEFAULT_DB_PORT = 5432
    DEFAULT_DB_DATABASE = 'ovirt_engine_history'
    DEFAULT_DB_USER = 'ovirt_engine_history'
    DEFAULT_DB_PASSWORD = ''
    DEFAULT_DB_SECURED = False
    DEFAULT_DB_SECURED_HOST_VALIDATION = False


@util.export
@util.codegen
class GrafanaDefaults(object):
    DEFAULT_DB_USER = 'ovirt_engine_history_grafana'
    DEFAULT_DB_PASSWORD = ''


@util.export
@util.codegen
class FileLocations(oengcommcons.FileLocations):
    GRAFANA_SYSCONF_DIR = config.GRAFANA_SYSCONF_DIR
    GRAFANA_STATE_DIR = config.GRAFANA_STATE_DIR
    GRAFANA_DATA_DIR = config.GRAFANA_DATA_DIR
    PKG_DATA_DIR = config.PKG_DATA_DIR

    GRAFANA_CONFIG_FILE = os.path.join(
        GRAFANA_SYSCONF_DIR,
        'grafana.ini',
    )
    GRAFANA_CONFIG_FILE_TEMPLATE = os.path.join(
        PKG_DATA_DIR,
        'conf',
        'grafana.ini.in',
    )
    GRAFANA_PROVISIONING_CONFIGURATION = os.path.join(
        GRAFANA_SYSCONF_DIR,
        'conf',
        'provisioning',
    )
    GRAFANA_PROVISIONING_DWH_DATASOURCE = os.path.join(
        GRAFANA_PROVISIONING_CONFIGURATION,
        'datasources',
        'ovirt-dwh.yaml',
    )
    GRAFANA_PROVISIONING_DWH_DATASOURCE_TEMPLATE = os.path.join(
        PKG_DATA_DIR,
        'conf',
        'grafana-dwh-data-source.template',
    )
    # This keeps Grafana user database credentials.
    # Nothing should use it except for engine-setup, which uses it to
    # keep them for future runs and for generating the datasource.
    OVIRT_ENGINE_DWHD_SERVICE_CONFIG_GRAFANA_DATABASE = os.path.join(
        odwhcons.FileLocations.OVIRT_ENGINE_DWHD_SERVICE_CONFIGD,
        '10-setup-grafana-database.conf',
    )
    HTTPD_CONF_GRAFANA = os.path.join(
        '/etc',
        'httpd',
        'conf.d',
        'ovirt-engine-grafana-proxy.conf'
    )
    HTTPD_CONF_GRAFANA_TEMPLATE = os.path.join(
        PKG_DATA_DIR,
        'conf',
        'httpd-grafana-proxy.conf.in'
    )
    # Grafana's (default) internal sqlite database, relative to
    # GRAFANA_STATE_DIR
    GRAFANA_DB = 'grafana.db'

    # PKI stuff. DIRs are taken from oengcommcons.FileLocations
    # which we inherit.

    # These are generated and used in case the engine-generated
    # apache pki is not found.
    OVIRT_ENGINE_PKI_GRAFANA_APACHE_KEY = os.path.join(
        oengcommcons.FileLocations.OVIRT_ENGINE_PKIKEYSDIR,
        '%s.key.nopass' % Const.PKI_GRAFANA_APACHE_CERT_NAME,
    )
    OVIRT_ENGINE_PKI_GRAFANA_APACHE_CA_CERT = os.path.join(
        oengcommcons.FileLocations.OVIRT_ENGINE_PKIDIR,
        '%s-ca.pem' % Const.PKI_GRAFANA_APACHE_CERT_NAME,
    )
    OVIRT_ENGINE_PKI_GRAFANA_APACHE_CERT = os.path.join(
        oengcommcons.FileLocations.OVIRT_ENGINE_PKICERTSDIR,
        '%s.cer' % Const.PKI_GRAFANA_APACHE_CERT_NAME,
    )

    OVIRT_ENGINE_SERVICE_CONFIG_GRAFANA = os.path.join(
        oenginecons.FileLocations.OVIRT_ENGINE_SERVICE_CONFIGD,
        '10-setup-grafana-access.conf'
    )


@util.export
class Stages(object):
    CORE_ENABLE = 'osetup.grafana.core.enable'
    DB_GRAFANA_CONNECTION_CUSTOMIZATION = \
        'osetup.grafana.db.connection.customization'
    DB_CONNECTION_SETUP = 'osetup.grafana.db.connection.setup'
    DB_PROVISIONING_CREATE_USER = 'osetup.grafana.db.provisioning.create_user'
    PKI_MISC = 'osetup.grafana.pki.misc'


@util.export
@util.codegen
@osetupattrsclass
class CoreEnv(object):

    @osetupattrs(
        answerfile=True,
        postinstallfile=True,
        summary=True,
        reconfigurable=True,
        description=_('Grafana integration'),
    )
    def ENABLE(self):
        return 'OVESETUP_GRAFANA_CORE/enable'


@util.export
@util.codegen
@osetupattrsclass
class ConfigEnv(object):
    GRAFANA_SERVICE_STOP_NEEDED = \
        'OVESETUP_GRAFANA_CONFIG/grafanaServiceStopNeeded'

    @osetupattrs(
        answerfile=True,
        is_secret=True,
    )
    def ADMIN_PASSWORD(self):
        return 'OVESETUP_GRAFANA_CONFIG/adminPassword'

    GRAFANA_PORT = 'OVESETUP_GRAFANA_CONFIG/GrafanaPort'
    HTTPD_CONF_GRAFANA = 'OVESETUP_GRAFANA_CONFIG/httpdConfGrafana'

    @osetupattrs(
        is_secret=True,
    )
    def CONF_SECRET_KEY(self):
        return 'OVESETUP_GRAFANA_CONFIG/confSecretKey'

    # This refers to grafana's internal database, which is
    # (also by default) an sqlite3 db file at
    # /var/lib/grafana/grafana.db . It's considered "new"
    # if it's missing or with size 0.
    NEW_DATABASE = 'OVESETUP_GRAFANA_CONFIG/newDatabase'

    GRAFANA_USER = 'OVESETUP_GRAFANA_CONFIG/grafanaUser'
    GRAFANA_GROUP = 'OVESETUP_GRAFANA_CONFIG/grafanaGroup'

    @osetupattrs(
        postinstallfile=True,
    )
    def GRAFANA_DB_CREATED_BY_US(self):
        return 'OVESETUP_GRAFANA_CORE/grafanaDbCreatedByUs'

    GRAFANA_FQDN = 'OVESETUP_GRAFANA_CONFIG/grafanaFQDN'

    KEY_SIZE = 'OVESETUP_GRAFANA_CONFIG/keySize'

    PKI_APACHE_CSR_FILENAME = 'OVESETUP_GRAFANA_CONFIG/pkiApacheCSRFilename'


@util.export
@util.codegen
@osetupattrsclass
class GrafanaDBEnv(object):

    @osetupattrs(
        answerfile=True,
        summary=True,
        description=_('Grafana database user name'),
    )
    def USER(self):
        return 'OVESETUP_GRAFANA_DB/user'

    @osetupattrs(
        answerfile=True,
    )
    def PASSWORD(self):
        return 'OVESETUP_GRAFANA_DB/password'

    CONNECTION = 'OVESETUP_GRAFANA_DB/connection'
    STATEMENT = 'OVESETUP_GRAFANA_DB/statement'


@util.export
@util.codegen
@osetupattrsclass
class RemoveEnv(object):
    pass


@util.export
@util.codegen
@osetupattrsclass
class RPMDistroEnv(object):
    ADDITIONAL_PACKAGES = 'OVESETUP_GRAFANA_RPMDISTRO/additionalPackages'
    PACKAGES_SETUP = 'OVESETUP_GRAFANA_RPMDISRO_PACKAGES_SETUP'


# vim: expandtab tabstop=4 shiftwidth=4
