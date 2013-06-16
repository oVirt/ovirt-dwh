#!/usr/bin/python -E
'''
provides an installer for ovirt-engine-dwh
'''

"""
TODO:
1. refactor shared code with ovirt-reports-setup to common_utils
2. check DB connectivity
3. enable command line options
4. refactor to share same UI as ovirt engine setup
"""

import logging
import sys
import os
import time
import traceback
import glob
import common_utils as utils
from decorators import transactionDisplay
log_file = None

DWH_PACKAGE_NAME="ovirt-engine-dwh"
PATH_DB_SCRIPTS="/usr/share/ovirt-engine-dwh/db-scripts"
PATH_WATCHDOG="/usr/share/ovirt-engine-dwh/etl/ovirt_engine_dwh_watchdog.cron"
EXEC_CREATE_DB="%s/ovirt-engine-history-db-install.sh" % PATH_DB_SCRIPTS
EXEC_UPGRADE_DB="upgrade.sh"
FILE_DB_CONN = "/etc/ovirt-engine/ovirt-engine-dwh/Default.properties"
FILE_ENGINE_CONF_DEFAULTS = "/usr/share/ovirt-engine/conf/engine.conf.defaults"
FILE_ENGINE_CONF = "/etc/ovirt-engine/engine.conf"
DB_BACKUPS_DIR = "/var/lib/ovirt-engine/backups"
DB_NAME = "ovirt_engine_history"
DB_USER_NAME = "postgres"
DB_PORT = "5432"
DB_HOST = "localhost"

# DB messages
DB_FILE = (
    "The DB was backed up as '{dbfile}'"
)
DB_RESTORE = (
    'The DB backup was created with compression. You must use "pg_restore" '
    'command if you need to recover the DB from the backup.'
)

#TODO: Create output messages file with all messages
#TODO: Move all errors here to make consistent usage
# ERRORS:
ERR_DB_CREATE_FAILED = "Error while trying to create %s db" % DB_NAME

log_file = utils.initLogging("%s-setup" % DWH_PACKAGE_NAME, "/var/log/ovirt-engine")

def dbExists(db_dict):
    logging.debug("checking if %s db already exists" % db_dict["name"])
    (output, rc) = utils.execSqlCmd(db_dict, "select 1")
    if (rc != 0):
        return False
    else:
        return True

@transactionDisplay("Creating DB")
def createDB(db_dict):
    """
    create fresh ovirt_engine_history db
    """
    logging.debug("installing %s db", DB_NAME)

    dbLogFilename = "ovirt-history-db-install-%s.log" %(utils.getCurrentDateTime())
    logging.debug("ovirt engine history db creation is logged at %s/%s" % ("/var/log/ovirt-engine", dbLogFilename))

    # Set ovirt-history-db-install.sh args - logfile
    if utils.localHost(db_dict["host"]):
        install_type = "local"
    else:
        install_type = "remote"
    cmd = [EXEC_CREATE_DB,
           "-l", dbLogFilename,
           "-u", db_dict["username"],
           "-s", db_dict["host"],
           "-p", db_dict["port"],
           "-r", install_type,
          ]

    # Create db using shell command
    output, rc = utils.execCmd(cmd, None, True, ERR_DB_CREATE_FAILED)
    logging.debug('Successfully installed %s DB' % db_dict["name"])

@transactionDisplay("Upgrade DB")
def upgradeDB(db_dict):
    """
    upgrade existing ovirt_engine_history db
    """
    logging.debug("upgrading %s db", DB_NAME)
    dbLogFilename = "ovirt-history-db-upgrade-%s.log" %(utils.getCurrentDateTime())
    logging.debug("ovirt engine history db upgrade is logged at %s/%s" % ("/var/log/ovirt-engine", dbLogFilename))

    # Try/Except so we'll be able to return to our current directory
    currDir = os.getcwd()
    try:
        cmd = [
                os.path.join(PATH_DB_SCRIPTS, EXEC_UPGRADE_DB),
                "-s", db_dict["host"],
                "-p", db_dict["port"],
                "-u", db_dict["username"],
                "-d", db_dict["name"],
                "-l", "/var/log/ovirt-engine/%s" % dbLogFilename,
              ]
        os.chdir(PATH_DB_SCRIPTS)
        output, rc = utils.execCmd(cmdList=cmd, failOnError=True, msg="Error while trying to upgrade %s DB" % DB_NAME)
    except:
        os.chdir(currDir)
        raise

def getDbDictFromOptions():
    db_dict = {"name"      : DB_NAME,
               "host"      : utils.getDbHostName(),
               "port"      : utils.getDbPort(),
               "username"  : utils.getDbAdminUser(),
               "password"  : utils.getPassFromFile(utils.getDbAdminUser())}
    return db_dict


@transactionDisplay("Setting DB connectivity")
def setDbPass(db_dict):
    '''
    set the password for the user postgres
    '''
    logging.debug("Setting DB pass")
    logging.debug("editing etl db connectivity file")

    file_handler = utils.TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    file_handler.editParam("ovirtEngineHistoryDbPassword", db_dict["password"])
    file_handler.editParam("ovirtEngineHistoryDbUser", db_dict["username"])
    file_handler.editParam("ovirtEngineDbPassword", db_dict["password"])
    file_handler.editParam("ovirtEngineDbUser", db_dict["username"])
    file_handler.editParam("ovirtEngineDbJdbcConnection",
                           "jdbc\:postgresql\://%s\:%s/engine?stringtype\=unspecified" % (db_dict["host"], db_dict["port"]))
    file_handler.editParam("ovirtEngineHistoryDbJdbcConnection",
                           "jdbc\:postgresql\://%s\:%s/%s?stringtype\=unspecified" % (db_dict["host"], db_dict["port"], db_dict["name"]))
    file_handler.close()

def isVersionSupported(rawMinimalVersion, rawCurrentVersion):
    """
    Check installed version with minimal support version
    """
    # Get current rpm version and parse it.
    (currentVersion, currentMinorVersion, currentRelease) = utils.parseVersionString(rawCurrentVersion)

    # Since minimalETLversion in vdc_options does not contain the "-something" release in its string. we add
    # it in order not to break the parseVersionString interface
    (minimalVersion, minimalMinorVersion, minimalRelease) = utils.parseVersionString("%s-0" % rawMinimalVersion)

    if (float(currentVersion) != float(minimalVersion)) or (int(currentMinorVersion) < int(minimalMinorVersion)):
        return False
    return True

def setVersion():
    """
    set the etlVersion option to current version
    """
    versionString = utils.getAppVersion(DWH_PACKAGE_NAME)
    (currentVersion, currentMinorVersion, currentRelease) = utils.parseVersionString(versionString)
    logging.debug("Setting etlVersion")
    logging.debug("editing etl connectivity file")
    file_handler = utils.TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    file_handler.editParam("etlVersion", "%s.%s" % (currentVersion, currentMinorVersion))
    file_handler.close()

def main():
    '''
    main
    '''
    rc = 0
    doBackup = None
    backupFile = None
    try:
        logging.debug("starting main()")

        db_dict = getDbDictFromOptions()

        # Get minimal supported version from oVirt Engine
        minimalVersion = utils.getVDCOption("MinimalETLVersion")
        currentVersion = utils.getAppVersion(DWH_PACKAGE_NAME)
        if not isVersionSupported(minimalVersion, currentVersion):
            print "Minimal supported version (%s) is higher then installed version (%s), please update the %s package" % (minimalVersion, currentVersion, DWH_PACKAGE_NAME)
            raise Exception("current version not supported by ovirt engine")

        # Stop engine
        if utils.stopEngine():

            # Stop ETL before doing anything
            utils.stopEtl()

            # Set DB connecitivty (user/pass)
            if db_dict['password']:
                setDbPass(db_dict)
            setVersion()

            # Create/Upgrade DB
            if dbExists(db_dict):
                try:
                    doBackup = utils.performBackup(db_dict, DB_BACKUPS_DIR)
                    backupFile = os.path.join(
                        DB_BACKUPS_DIR,
                        'ovirt-engine-history.backup.{date}'.format(
                            date=utils.getCurrentDateTime(),
                        )
                    )
                    if doBackup:
                        utils.backupDB(
                            backupFile,
                            db_dict,
                        )
                except UserWarning:
                    print 'User decided to stop setup. Exiting.'
                    # Start Services
                    utils.startEngine()
                    # Sleep for 20 secs to allow health applet to start
                    time.sleep(20)
                    utils.startEtl()
                    sys.exit(0)

                # Backup went ok, so upgrade
                upgradeDB(db_dict)
            else:
                createDB(db_dict)

            # Start Services
            utils.startEngine()
            # Sleep for 20 secs to allow health applet to start
            time.sleep(20)
            utils.startEtl()

            print "Successfully installed %s." % DWH_PACKAGE_NAME
            print "The installation log file is available at: %s" % log_file
            if doBackup:
                print DB_FILE.format(
                    dbfile=backupFile
                )
                print DB_RESTORE
        else:
            logging.debug("user chose not to stop engine")
            print "Installation stopped, Goodbye."

        logging.debug("main() ended")
    except:
        logging.error("Exception caught!")
        logging.error(traceback.format_exc())
        print "Error encountered while installing %s, please consult the log file: %s" % (DWH_PACKAGE_NAME,log_file)
        rc = 1
    finally:
        return rc

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
