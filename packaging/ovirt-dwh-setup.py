#!/usr/bin/python -E
'''
provides an installer for ovirt-dwh
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
import traceback
import common_utils as utils
from decorators import transactionDisplay
log_file = None

PATH_DB_SCRIPTS="/usr/share/ovirt-dwh/db-scripts"
PATH_WATCHDOG="/usr/share/ovirt-dwh/etl/ovirt_etl_watchdog.cron"
EXEC_CREATE_DB="%s/ovirt-history-db-install.sh" % PATH_DB_SCRIPTS
EXEC_UPGRADE_DB="upgrade.sh"
FILE_DB_CONN = "/etc/ovirt/ovirt-dwh/Default.properties"
FILE_PG_PASS="/root/.pgpass"
DB_USER_NAME = "postgres"

log_file = utils.initLogging("ovirt-dwh-setup", "/var/log/ovirt")

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
    create fresh ovirt_history db
    """
    logging.debug("installing ovirt_history db")

    dbLogFilename = "ovirt-history-db-install-%s.log" %(utils.getCurrentDateTime())
    logging.debug("ovirt history db creation is logged at %s/%s" % ("/var/log/ovirt", dbLogFilename))

    # Set ovirt-history-db-install.sh args - logfile
    cmd = "/bin/sh %s %s " % (EXEC_CREATE_DB, dbLogFilename)
    output, rc = utils.execExternalCmd(cmd, True, "Error while trying to create ovirt_history DB")
    logging.debug('Successfully installed %s ovirt_history')

@transactionDisplay("Upgrade DB")
def upgradeDB(db_dict):
    """
    upgrade existing ovirt_history db
    """
    logging.debug("upgrading ovirt_history db")

    # Try/Except so we'll be able to return to our current directory
    currDir = os.getcwd()
    try:
        cmd = "sh ./%s" % EXEC_UPGRADE_DB
        os.chdir(PATH_DB_SCRIPTS)
        output, rc = utils.execExternalCmd(cmd, True, "Error while trying to upgrade ovirt_history DB") 
    except:
        os.chdir(currDir)
        raise

def getDbDictFromOptions():
    db_dict = {"name"      : "ovirt_history",
               "host"      : None,
               "username"  : "postgres",
               "password"  : None}
    return db_dict

def getPassFromFile(username):
    '''
    get the password for specified user
    from /root/.pgpass
    '''
    db_pass = None
    logging.debug("getting DB password for %s" % username)
    fd = open(FILE_PG_PASS, "r")
    for line in fd:
        if line.startswith("#"):
            continue
        list = line.split(":")
        if list[3] == username:
            logging.debug("found password for username %s" % username)
            db_pass = list[4].rstrip('\n')
    fd.close()
    return db_pass

def setDbPass(password):
    '''
    set the password for the user postgres
    '''
    logging.debug("Setting DB pass")
    logging.debug("editing etl db connectivity file")
    file_handler = utils.TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    file_handler.editParam("ovirtHistoryDbPassword", password)
    file_handler.editParam("ovirtEngineDbPassword", password)
    file_handler.close()

@transactionDisplay("Setting DB connectivity")
def setDBConn(dbUserName):
    db_pass = getPassFromFile(dbUserName)
    if db_pass:
        setDbPass(db_pass)

def isVersionSupported(rawMinimalVersion, rawCurrentVersion):
    """
    Check installed version with minimal support version
    """
    # Get current rpm version and parse it.
    (currentVersion, currentMinorVersion, currentRelease) = utils.parseVersionString(rawCurrentVersion)

    # Since minimalETLversion in vdc_options does not contain the "-something" release in its string. we add
    # it in order not to break the parseVersionString interface
    (minimalVersion, minimalMinorVersion, minimalRelease) = utils.parseVersionString("%s-0" % rawMinimalVersion)

    if (float(currentVersion) < float(minimalVersion)) or (int(currentMinorVersion) < int(minimalMinorVersion)):
        return False
    
    return True 

def setVersion():
    """
    set the etlVersion option to current version
    """
    versionString = utils.getAppVersion("ovirt-dwh")
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
    try:
        logging.debug("starting main()")

        db_dict = getDbDictFromOptions()

        # Get minimal supported version from oVirt Engine
        minimalVersion = utils.getVDCOption("MinimalETLVersion")
        currentVersion = utils.getAppVersion("ovirt-dwh")
        
        if not isVersionSupported(minimalVersion, currentVersion):
            print "Minimal supported version (%s) is higher then installed version (%s), please update the ovirt-dwh package" % (minimalVersion, currentVersion)
            raise Exception("current version not supported by ovirt engine")

        # Stop JBOSSAS
        if utils.stopJboss():

            # Stop ETL before doing anything
            utils.stopEtl()

            # Set DB connecitivty (user/pass)
            setDBConn(DB_USER_NAME)
            setVersion()

            # Create/Upgrade DB
            if dbExists(db_dict):
                upgradeDB(db_dict)
            else:
                createDB(db_dict)

            # Start Services
            utils.startJboss()
            utils.startEtl()

            print "Successfully installed ovirt-dwh."
            print "The installation log file is available at: %s" % log_file
        else:
            logging.debug("user chose not to stop jboss")
            print "Installation stopped, Goodbye."

        logging.debug("main() ended")
    except:
        logging.error("Exception caught!")
        logging.error(traceback.format_exc())
        print "Error encountered while installing ovirt-dwh, please consult the log file: %s" % log_file
        rc = 1
    finally:
         return rc

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
