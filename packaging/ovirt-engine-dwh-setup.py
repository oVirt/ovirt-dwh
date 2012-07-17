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
import re
import traceback
import common_utils as utils
from decorators import transactionDisplay
log_file = None

PATH_DB_SCRIPTS="/usr/share/ovirt-engine-dwh/db-scripts"
PATH_WATCHDOG="/usr/share/ovirt-engine-dwh/etl/ovirt_engine_dwh_watchdog.cron"
EXEC_CREATE_DB="%s/ovirt-engine-history-db-install.sh" % PATH_DB_SCRIPTS
EXEC_UPGRADE_DB="upgrade.sh"
FILE_DB_CONN = "/etc/ovirt-engine/ovirt-engine-dwh/Default.properties"
FILE_WEB_CONF = "/etc/ovirt-engine/web-conf.js"
FILE_PG_PASS="/root/.pgpass"
DB_USER_NAME = "postgres"
DB_PORT = "5432"
DB_HOST = "localhost"

#TODO: Create output messages file with all messages
#TODO: Move all errors here to make consistent usage
# ERRORS:
ERR_DB_CREATE_FAILED = "Error while trying to create ovirt_engine_history db"

log_file = utils.initLogging("ovirt-engine-dwh-setup", "/var/log/ovirt-engine")

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
    logging.debug("installing ovirt_engine_history db")

    dbLogFilename = "ovirt-history-db-install-%s.log" %(utils.getCurrentDateTime())
    logging.debug("ovirt engine history db creation is logged at %s/%s" % ("/var/log/ovirt", dbLogFilename))

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
    logging.debug("upgrading ovirt_engine_history db")

    # Try/Except so we'll be able to return to our current directory
    currDir = os.getcwd()
    try:
        cmd = "sh ./%s" % EXEC_UPGRADE_DB
        os.chdir(PATH_DB_SCRIPTS)
        output, rc = utils.execExternalCmd(cmd, True, "Error while trying to upgrade ovirt_engine_history DB")
    except:
        os.chdir(currDir)
        raise

def getDbDictFromOptions():
    db_dict = {"name"      : "ovirt_engine_history",
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

    (fqdn, port) = getHostParams()

    file_handler = utils.TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    file_handler.editParam("ovirtEngineHistoryDbPassword", db_dict["password"])
    file_handler.editParam("ovirtEngineHistoryDbUser", db_dict["username"])
    file_handler.editParam("ovirtEngineDbPassword", db_dict["password"])
    file_handler.editParam("ovirtEngineDbUser", db_dict["username"])
    file_handler.editParam("ovirtEngineDbJdbcConnection",
                           "jdbc\:postgresql\://%s\:%s/engine?stringtype\=unspecified" % (db_dict["host"], db_dict["port"]))
    file_handler.editParam("ovirtEngineHistoryDbJdbcConnection",
                           "jdbc\:postgresql\://%s\:%s/ovirt_engine_history?stringtype\=unspecified" % (db_dict["host"], db_dict["port"]))
    file_handler.editParam("ovirtEnginePortalPort", port)
    file_handler.close()

def getHostParams(secure=False):
    """
    get hostname & secured port from /etc/ovirt-engine/web-conf.js
    """

    pattern = "var\shttp_port\s\=\s\"(\d+)\""
    if secure:
        pattern = "var\shttps_port\s\=\s\"(\d+)\""

    logging.debug("looking for configuration from %s", FILE_WEB_CONF)
    if not os.path.exists(FILE_WEB_CONF):
        raise Exception("Could not find %s" % FILE_WEB_CONF)

    logging.debug("reading %s", FILE_WEB_CONF)
    fileObj = open(FILE_WEB_CONF, "r")
    hostFqdn = None
    port = None

    logging.debug("Itterating over file")
    for line in fileObj.readlines():
        # var host_fqdn = "vm-18-12.eng.lab.tlv.redhat.com";
        line = line.strip()
        found = re.search("var\shost_fqdn\s\=\s\"(\S+)\"", line)
        if found:
            hostFqdn = found.group(1)
            logging.debug("host fqdn is: %s", hostFqdn)
        # var http/https_port = "9443";
        found = re.search(pattern, line)
        if found:
            port = found.group(1)
            if secure:
                logging.debug("Secure web port is: %s", port)
            else:
                logging.debug("Web port is: %s", port)


    fileObj.close()

    if not hostFqdn:
        logging.error("Could not find the HOST FQDN from %s", FILE_WEB_CONF)
        raise Exception("Cannot find host fqdn from configuration, please verify that ovirt-engine is configured")
    if not port:
        logging.error("Could not find the web port from %s", FILE_WEB_CONF)
        raise Exception("Cannot find the web port from configuration, please verify that ovirt-engine is configured")

    return (hostFqdn, port)

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
    versionString = utils.getAppVersion("ovirt-engine-dwh")
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
        currentVersion = utils.getAppVersion("ovirt-engine-dwh")
        if not isVersionSupported(minimalVersion, currentVersion):
            print "Minimal supported version (%s) is higher then installed version (%s), please update the ovirt-engine-dwh package" % (minimalVersion, currentVersion)
            raise Exception("current version not supported by ovirt engine")

        # Stop JBOSSAS
        if utils.stopJboss():

            # Stop ETL before doing anything
            utils.stopEtl()

            # Set DB connecitivty (user/pass)
            if db_dict['password']:
                setDbPass(db_dict)
            setVersion()

            # Create/Upgrade DB
            if dbExists(db_dict):
                upgradeDB(db_dict)
            else:
                createDB(db_dict)

            # Start Services
            utils.startJboss()
            utils.startEtl()

            print "Successfully installed ovirt-engine-dwh."
            print "The installation log file is available at: %s" % log_file
        else:
            logging.debug("user chose not to stop jboss")
            print "Installation stopped, Goodbye."

        logging.debug("main() ended")
    except:
        logging.error("Exception caught!")
        logging.error(traceback.format_exc())
        print "Error encountered while installing ovirt-engine-dwh, please consult the log file: %s" % log_file
        rc = 1
    finally:
        return rc

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
