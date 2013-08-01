#!/usr/bin/python
'''
common utils for rhev-dwh-setup
'''

import csv
import getpass
import logging
import os
import pwd
import grp
import traceback
import datetime
import time
import re
from StringIO import StringIO
import subprocess
import shutil
from decorators import transactionDisplay
import tempfile
import random
import string

#text colors
RED = "\033[0;31m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
NO_COLOR = "\033[0m"
ENGINE_SERVICE_NAME = "ovirt-engine"

# CONST
EXEC_IP = "/sbin/ip"
EXEC_PSQL = '/usr/bin/psql'
EXEC_SU = '/bin/su'
EXEC_PGDUMP = '/usr/bin/pg_dump'
FILE_PG_PASS="/etc/ovirt-engine/.pgpass"
EXEC_SERVICE="/sbin/service"

FILE_DB_CONN="/etc/ovirt-engine/engine.conf.d/10-setup-database.conf"
PGPASS_FILE_USER_LINE = "DB USER credentials"
PGPASS_FILE_ADMIN_LINE = "DB ADMIN credentials"
FILE_ENGINE_CONFIG_BIN="/usr/bin/engine-config"
FILE_DATABASE_CONFIG = "/etc/ovirt-engine/engine.conf.d/10-setup-database.conf"
READ_ONLY_UPDATE_SQLFILE = '/tmp/updateReadOnly.sql'

# ERRORS
# TODO: Move all errors here and make them consistent
ERR_EXP_GET_CFG_IPS = "Error: could not get list of available IP addresses on this host"
ERR_EXP_GET_CFG_IPS_CODES = "Error: failed to get list of IP addresses"
ERR_RC_CODE = "Error: return Code is not zero"
ERR_WRONG_PGPASS_VALUE = "Error: unknown value type '%s' was requested"
ERR_PGPASS_VALUE_NOT_FOUND = "Error: requested value '%s' was not found \
in %s. Check oVirt Engine installation and that wildcards '*' are not used."
ERR_DB_GET_SPACE = "Error: Failed to get %s database size."

# DB defaults
DB_HOST = "localhost"
DB_PORT = "5432"
DB_ADMIN = "postgres"

# DB related messages
DB_BACKUP_HEADER = (
    '\nExisting DB was found on the system. The size of the detected DB '
    'is {dbsize} Mb, free space in the backup folder {backup} '
    'is {foldersize} Mb. \n'
)

DB_BACKUP_SHOW_STOP = (
    '\nThere is not enough free space in the backup folder {backup} to backup '
    'the existing database. Would you like to proceed without backup?\n'
    'Answering "no" will stop the upgrade'
)
DB_BACKUP_SHOW_CONTINUE = (
    '\nThe upgrade utility can backup the existing database. The time and '
    'space required for the database backup depend on its size. The detected '
    'DB size is {dbsize} Mb. This process can take a considerable time, and in '
    'some cases may take few hours to complete. Would you like to continue '
    'and backup the existing database?\n'
    'Answering "no" will skip the backup step and continue the upgrade '
    'without backing up the database'
)
DB_BACKUP_CONTINUE_WITH = (
    'Are you sure you would like to continue '
    'and backup database {db}?\n'
    'Answering "no" will stop the upgrade'
)
DB_BACKUP_CONTINUE_WITHOUT = (
    'Are you sure you would like to continue '
    'and SKIP the backup of the database {db}?\n'
    'Answering "no" will stop the upgrade'
)
DB_RESTORE = (
    'The DB backup was created with compression. You must use "pg_restore" '
    'command if you need to recover the DB from the backup.\n'
)

# File locations
DIR_PGSQL_DATA = '/var/lib/pgsql/data'
FILE_POSTGRES_CONF = os.path.join(
    DIR_PGSQL_DATA,
    'postgresql.conf'
)
FILE_PG_HBA = os.path.join(
    DIR_PGSQL_DATA,
    'pg_hba.conf'
)
FILE_SERVER_KEY = os.path.join(
    DIR_PGSQL_DATA,
    'server.key'
)
FILE_SERVER_CERTIFICATE = os.path.join(
    DIR_PGSQL_DATA,
    'server.crt'
)
FILE_ENGINE_CERT = '/etc/pki/ovirt-engine/ca.pem'
FILE_ENGINE_PRIVATE = '/etc/pki/ovirt-engine/private/ca.pem'

def _maskString(string, maskList=[]):
    """
    private func to mask passwords
    in utils
    """
    maskedStr = string
    for maskItem in maskList:
        maskedStr = maskedStr.replace(maskItem, "*"*8)

    return maskedStr

def getVDCOption(key):
    """
    Get option_value from vdc_options per given key
    """
    cmd = [
        FILE_ENGINE_CONFIG_BIN,
        "-g",
        key,
        "--cver=general",
        "-p",
        "/usr/share/ovirt-engine/conf/engine-config-install.properties",
    ]
    logging.debug("getting vdc option %s" % key)

    output, rc = execCmd(cmdList=cmd, failOnError=True, msg="Error: failed fetching configuration field %s" % key)
    logging.debug("Value of %s is %s" % (key, output))

    return output.rstrip()

def _getColoredText (text, color):
    ''' gets text string and color
        and returns a colored text.
        the color values are RED/BLUE/GREEN/YELLOW
        everytime we color a text, we need to disable
        the color at the end of it, for that
        we use the NO_COLOR chars.
    '''
    return color + text + NO_COLOR

def getCurrentDateTime(is_utc=None):
    '''
    provides current date
    '''
    now = None
    if (is_utc is not None):
        now = datetime.datetime.utcnow()
    else:
        now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M_%S")

def initLogging(baseFileName, baseDir):
    '''
    initiates logging
    '''
    try:
        #in order to use UTC date for the log file, send True to getCurrentDateTime(True)
        log_file_name = "%s-%s.log" %(baseFileName, getCurrentDateTime())
        log_file = os.path.join(baseDir, log_file_name)
        if not os.path.isdir(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        level = logging.INFO
        level = logging.DEBUG
        hdlr = logging.FileHandler(filename = log_file, mode='w')
        fmts = '%(asctime)s::%(levelname)s::%(module)s::%(lineno)d::%(name)s:: %(message)s'
        dfmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter(fmts, dfmt)
        hdlr.setFormatter(fmt)
        logging.root.addHandler(hdlr)
        logging.root.setLevel(level)
        return log_file
    except:
        logging.error(traceback.format_exc())
        raise Exception()

class ConfigFileHandler:
    def __init__(self, filepath):
        self.filepath = filepath
    def open(self):
        pass
    def close(self):
        pass
    def editParams(self, paramsDict):
        pass
    def delParams(self, paramsDict):
        pass

class TextConfigFileHandler(ConfigFileHandler):
    def __init__(self, filepath, sep='='):
        ConfigFileHandler.__init__(self, filepath)
        self.data = []
        self.sep = sep

    def open(self):
        fd = file(self.filepath)
        self.data = fd.readlines()
        fd.close()

    def close(self):
        fd = file(self.filepath, 'w')
        for line in self.data:
            fd.write(line)
        fd.close()

    def getParam(self, param):
        value = None
        for line in self.data:
            if not re.match("\s*#", line):
                found = re.match("\s*%s\s*\%s\s*(.+)$" % (param, self.sep), line)
                if found:
                    value = found.group(1)
        return value

    def editParam(self, param, value):
        changed = False
        for i, line in enumerate(self.data[:]):
            if not re.match("\s*#", line):
                if re.match("\s*%s"%(param), line):
                    self.data[i] = "%s%s%s\n"%(param, self.sep, value)
                    changed = True
                    break
        if not changed:
            self.data.append("%s%s%s\n"%(param, self.sep, value))

    def renameParam(self, current_param_name, new_param_name):
        if current_param_name == new_param_name:
            return
        changed = False
        for i, line in enumerate(self.data[:]):
            if not re.match("\s*#", line):
                if re.match("\s*%s"%(new_param_name), line):
                    changed = True
                    break
                if re.match("\s*%s"%(current_param_name), line):
                    self.data[i] = line.replace(current_param_name, new_param_name)
                    changed = True
                    break
        if not changed:
            self.data.append("%s%s\n"%(new_param_name, self.sep))

    def delParams(self, paramsDict):
        pass

def askQuestion(question=None, yesNo=False, options=''):
    '''
    provides an interface that prompts the user
    to answer "yes/no" to a given question
    '''
    message = StringIO()
    if yesNo:
        options = '(yes|no)'
    ask_string = "{question} {options}: ".format(
        question=question,
        options=options,
    )
    logging.debug("asking user: %s" % ask_string)
    message.write(ask_string)
    message.seek(0)
    raw_answer = raw_input(message.read())
    logging.debug("user answered: %s"%(raw_answer))
    answer = raw_answer.lower()
    if yesNo:
        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            return askQuestion(question, yesNo=True)
    else:
        return answer or askQuestion(question, options)

def askYesNo(question=None):
    '''
    provides an interface that prompts the user
    to answer "yes/no" to a given question
    '''
    return askQuestion(question, yesNo=True)


def parseRemoteSqlCommand(db_dict, sqlQuery, failOnError=False, errMsg='Failed running sql query', envDict={}):
    ret = []
    sqlQuery = "copy (%s) to stdout with csv header;" % sqlQuery.replace(";", "")
    out, rc = execSqlCmd(
        db_dict,
        sqlQuery,
        failOnError,
        errMsg,
        envDict,
    )
    if rc == 0:
        # we want reusable list, so load all into memory
        ret = [x for x in csv.DictReader(out.splitlines(True))]

    return ret, rc

def execSqlCmd(db_dict, sql_query, fail_on_error=False, err_msg="Failed running sql query", envDict={}):
    logging.debug("running sql query on host: %s, port: %s, db: %s, user: %s, query: \'%s\'." %
                  (db_dict["host"],
                   db_dict["port"],
                   db_dict["name"],
                   db_dict["username"],
                   sql_query))
    cmd = [
        EXEC_PSQL,
        "--pset=tuples_only=on",
        "--set",
        "ON_ERROR_STOP=1",
        "--dbname", db_dict["name"],
        "--host", db_dict["host"],
        "--port", db_dict["port"],
        "--username", db_dict["username"],
        "-w",
        "-c", sql_query,
    ]
    return execCmd(cmdList=cmd, failOnError=fail_on_error, msg=err_msg, envDict=envDict)

def isEngineUp():
    '''
    checks if ovirt-engine is active
    '''
    logging.debug("checking the status of ovirt-engine")
    cmd = [
        EXEC_SERVICE,
        ENGINE_SERVICE_NAME,
        'status',
    ]
    output, rc = execCmd(cmdList=cmd, msg="Failed while checking for ovirt-engine service status")
    if " is running" in output:
        return True
    else:
        return False

def stopEngine():
    '''
    stops the ovirt-engine service
    '''
    logging.debug("checking ovirt-engine service")
    if isEngineUp():
        logging.debug("ovirt-engine is up and running")
        print "In order to proceed the installer must stop the ovirt-engine service"
        answer = askYesNo("Would you like to stop the ovirt-engine service")
        if answer:
            stopEngineService()
        else:
            logging.debug("User chose not to stop ovirt-engine")
            return False
    return True

@transactionDisplay("Stopping ovirt-engine")
def stopEngineService():
    logging.debug("Stopping ovirt-engine")
    cmd = [EXEC_SERVICE, ENGINE_SERVICE_NAME, "stop"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to stop the ovirt-engine service")

def startEngine():
    '''
    starts the ovirt-engine service
    '''
    if not isEngineUp():
        startEngineService()
    else:
        logging.debug("jobss is up. nothing to start")

@transactionDisplay("Starting ovirt-engine")
def startEngineService():
    logging.debug("Starting ovirt-engine")
    cmd = [EXEC_SERVICE, ENGINE_SERVICE_NAME, "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the ovirt-engine service")

def isPostgresUp():
    '''
    checks if the postgresql service is up and running
    '''
    logging.debug("checking the status of postgresql")
    cmd = [EXEC_SERVICE, "postgresql", "status"]
    output, rc = execCmd(cmd)
    if rc == 0:
        return True
    else:
        return False

def startPostgres():
    '''
    starts the postgresql service
    '''
    if not isPostgresUp():
        startPostgresService()

def stopPostgres():
    '''
    stops the postgresql service
    '''
    if isPostgresUp():
        stopPostgresService()

def startPostgresService():
    logging.debug("starting postgresql")
    cmd = [EXEC_SERVICE, "postgresql", "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the postgresql service")

def stopPostgresService():
    logging.debug("stopping postgresql")
    cmd = [EXEC_SERVICE, "postgresql", "stop"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to stop the postgresql service")

def stopEtl():
    """
    stop the ovirt-engine-dwhd service
    """
    logging.debug("Stopping ovirt-engine-dwhd")
    cmd = [EXEC_SERVICE, "ovirt-engine-dwhd", "stop"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to stop the ovirt-engine-dwhd service")

def startEtl():
    '''
    starts the ovirt-engine-dwhd service
    '''
    enableEtlService()
    if not isEtlUp():
        startEtlService()
    else:
        logging.debug("ovirt-engine-dwhd is up. no need to start it")

def enableEtlService():
    """
    enable the ovirt-engine-dwhd service
    """
    cmd = ["/sbin/chkconfig", "ovirt-engine-dwhd", "on"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while attempting to enable the ovirt-engine-dwhd service")

@transactionDisplay("Starting oVirt-ETL")
def startEtlService():
    logging.debug("Starting ovirt-engine-dwhd")
    cmd = [EXEC_SERVICE, "ovirt-engine-dwhd", "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the ovirt-engine-dwhd service")

def isEtlUp():
    '''
    checks if ovirt-engine-dwhd is active
    '''
    logging.debug("checking the status of ovirt-engine-dwhd")
    cmd = [EXEC_SERVICE, "ovirt-engine-dwhd", "status"]
    output, rc = execCmd(cmd)
    if rc == 1:
        return False
    else:
        return True

def copyFile(source, destination):
    '''
    copies a file
    '''
    logging.debug("copying %s to %s" % (source, destination))
    shutil.copy2(source,destination)

def parseVersionString(string):
    """
    parse ovirt engine version string and seperate it to version, minor version and release
    """
    VERSION_REGEX="(\d+\.\d+)\.(\d+)\-(\d+)"
    logging.debug("setting regex %s againts %s" % (VERSION_REGEX, string))
    found = re.search(VERSION_REGEX, string)
    if not found:
        raise Exception("Cannot parse version string, please report this error")
    version = found.group(1)
    logging.debug("found version, %s", version)
    minorVersion= found.group(2)
    logging.debug("found minorVersion %s", minorVersion)
    release = found.group(3)
    logging.debug("found release %s", release)

    return (version, minorVersion, release)

def getAppVersion(package):
    '''
    get the installed package version
    '''
    cmd = [
        "rpm",
        "-q",
        "--queryformat", "%{VERSION}-%{RELEASE}",
        package,
    ]
    output, rc = execCmd(cmdList=cmd, failOnError=True, msg="Failed to get package version & release")
    return output.rstrip()

def dbExists(db_dict):
    logging.debug("checking if %s db already exists" % db_dict["name"])
    (output, rc) = execSqlCmd(db_dict, "select 1")
    if (rc != 0):
        return False
    else:
        return True

def getDbAdminUser():
    """
    Retrieve Admin user from config file on the system.
    Use default settings if file is not found.
    """
    file_handler = TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    return file_handler.getParam('ENGINE_DB_USER') or DB_ADMIN

def getDbHostName():
    """
    Retrieve DB Host name from .pgpass file on the system.
    Use default settings if file is not found, or '*' was used.
    """
    file_handler = TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    return file_handler.getParam('ENGINE_DB_HOST') or DB_HOST

def getDbPort():
    """
    Retrieve DB port number from .pgpass file on the system.
    """
    file_handler = TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    return file_handler.getParam('ENGINE_DB_PORT') or DB_PORT

def getPassFromFile():
    '''
    get the DB password
    '''
    file_handler = TextConfigFileHandler(FILE_DB_CONN)
    file_handler.open()
    return file_handler.getParam('ENGINE_DB_PASSWORD')

def dropDB(db_dict):
    """
    drops the given DB
    """
    logging.debug("dropping db %s" % db_dict["name"])
    cmd = [
        "/usr/bin/dropdb",
        "-U", db_dict["username"],
        db_dict["name"],
    ]
    (output, rc) = execCmd(cmdList=cmd, failOnError=True, msg="Error while removing database %s" % db_dict["name"])

def getConfiguredIps():
    try:
        iplist=set()
        cmd = [EXEC_IP, "addr"]
        output, rc = execCmd(cmdList=cmd, failOnError=True, msg=ERR_EXP_GET_CFG_IPS_CODES)
        ipaddrPattern=re.compile('\s+inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+')
        list=output.splitlines()
        for line in list:
            foundIp = ipaddrPattern.search(line)
            if foundIp:
                if foundIp.group(1) != "127.0.0.1":
                    ipAddr = foundIp.group(1)
                    logging.debug("Found IP Address: %s"%(ipAddr))
                    iplist.add(ipAddr)
        return iplist
    except:
        logging.error(traceback.format_exc())
        raise Exception(ERR_EXP_GET_CFG_IPS)

def localHost(hostname):
    # Create an ip set of possible IPs on the machine. Set has only unique values, so
    # there's no problem with union.
    # TODO: cache the list somehow? There's no poing quering the IP configuraion all the time.
    ipset = getConfiguredIps().union(set([ "localhost", "127.0.0.1"]))
    if hostname in ipset:
        return True
    return False

def createReadOnlyUser(db_dict, PGPASS_FILE):

    # Check whether we can create DB:
    global DB_ADMIN
    canCreateDb = False
    errorMsg = None

    canCreateDb = testLocalDb()

    if not canCreateDb:
        return (False, errorMsg)

    # Ask user how would the user be created
    createReadUser = askYesNo(
        question=(
            '\nThis utility can configure a read only user for DB access. '
            'Would you like to do so?'
        )
    )

    if not createReadUser:
        logging.debug('Skipping creation of read only DB user.')
        print 'Skipping creationg of read only DB user.'
        return (True, '')

    user = askQuestion(
        question='Provide a username for read-only user'
    )

    password = getpass.getpass(
        prompt='Provide a password for read-only user: '
    )

    secured = askYesNo(
        question=(
            'Should postgresql be setup with secure connection?'
        )
    )

    updatePgHba(db_dict['name'], user)
    configurePostgres(user, secured)
    if secured:
        createCertificate()
    restartPostgres()
    createUser(
        user=user,
        password=password,
        database=db_dict['name'],
    )
    updateReadOnly(
        user=user,
        database=db_dict['name'],
    )
    return (True, '')


def configurePostgres(user, secured):
    with open(FILE_POSTGRES_CONF, 'r') as f:
        configured_network = False
        configured_ssl = False
        content = []
        for line in f.read().splitlines():
            if (
                not configured_network and
                line.startswith('#listen_addresses')
            ):
                content.append("listen_addresses = '*'")
                configured_network = True

            if (
                secured and
                not configured_ssl and
                line.startswith('#ssl')
            ):
                content.append("ssl = on")
                configured_ssl = True

            if line.startswith('listen_addresses'):
                if '*' in line:
                    break
                else:
                    line = '#' + line

            content.append(line)

    # TODO: backup!!!
    with open(FILE_POSTGRES_CONF, 'w') as f:
        f.write('\n'.join(content))


def createCertificate():
    cmds =(
        [
            'openssl',
            'x509',
            '-in', FILE_ENGINE_CERT,
            '-out', FILE_SERVER_CERTIFICATE,
        ],
        [
            'openssl',
            'rsa',
            '-in', FILE_ENGINE_PRIVATE,
            '-out', FILE_SERVER_KEY,
        ],
    )
    for cmd in cmds:
        execCmd(
            cmdList=cmd,
            cwd=DIR_PGSQL_DATA,
            failOnError=True,
            msg='Failed to create self-signed certificate for postgresql server'
        )

    for f in (
        FILE_SERVER_KEY,
        FILE_SERVER_CERTIFICATE,
    ):
        if os.path.exists(f):
            os.chown(
                f,
                getUsernameId('postgres'),
                getGroupId('postgres')
            )

            if f == FILE_SERVER_KEY:
                os.chmod(
                    FILE_SERVER_KEY,
                    0o600
                )


def restartPostgres():
    stopPostgres()
    startPostgres()

#TODO: Move all execution commands to execCmd
def execCmd(
        cmdList,
        cwd=None,
        failOnError=False,
        msg='Return Code is not zero',
        maskList=[],
        useShell=False,
        usePipeFiles=False,
        envDict=None
    ):
    """
    Run external shell command with 'shell=false'
    receives a list of arguments for command line execution
    """
    # All items in the list needs to be strings, otherwise the subprocess will fail
    cmd = [str(item) for item in cmdList]

    # We need to join cmd list into one string so we can look for passwords in it and mask them
    logCmd = _maskString((' '.join(cmd)), maskList)

    logging.debug("Executing command --> '%s' in working directory '%s'" % (logCmd, cwd or os.getcwd()))

    stdErrFD = subprocess.PIPE
    stdOutFD = subprocess.PIPE
    stdInFD = subprocess.PIPE

    if usePipeFiles:
        (stdErrFD, stdErrFile) = tempfile.mkstemp(dir="/tmp")
        (stdOutFD, stdOutFile) = tempfile.mkstemp(dir="/tmp")
        (stdInFD, stdInFile) = tempfile.mkstemp(dir="/tmp")

    # Copy os.environ and update with envDict if provided
    env = os.environ.copy()
    env.update(envDict or {})
    if "ENGINE_PGPASS" in env.keys():
        env["PGPASSFILE"] = env["ENGINE_PGPASS"]
    else:
        env["PGPASSFILE"] = FILE_PG_PASS

    # We use close_fds to close any file descriptors we have so it won't be copied to forked childs
    proc = subprocess.Popen(
        cmd,
        stdout=stdOutFD,
        stderr=stdErrFD,
        stdin=stdInFD,
        cwd=cwd,
        shell=useShell,
        close_fds=True,
        env=env,
    )

    out, err = proc.communicate()
    if usePipeFiles:
        with open(stdErrFile, 'r') as f:
            err = f.read()
        os.remove(stdErrFile)

        with open(stdOutFile, 'r') as f:
            out = f.read()
        os.remove(stdOutFile)
        os.remove(stdInFile)

    logging.debug("output = %s"%(out))
    logging.debug("stderr = %s"%(err))
    logging.debug("retcode = %s"%(proc.returncode))
    output = out + err
    if failOnError and proc.returncode != 0:
        raise Exception(msg)
    return ("".join(output.splitlines(True)), proc.returncode)


def getAvailableSpace(path):
    logging.debug("Checking available space on %s" % (path))
    stat = os.statvfs(path)
    #block size * available blocks = available space in bytes, we devide by
    #1024 ^ 2 in order to get the size in megabytes
    availableSpace = (stat.f_bsize * stat.f_bavail) / pow(20, 2)
    logging.debug("Available space on %s is %s" % (path, availableSpace))
    return int(availableSpace)


def getDbSize(db_dict, PGPASS_FILE):
    # Returns db size in MB
    sql = "SELECT pg_database_size(\'%s\')" % db_dict['name']

    # Work with db credentials copy, rename db name to template1
    db_copy = db_dict.copy()
    db_copy['name'] = 'template1'
    out, rc = parseRemoteSqlCommand(
        db_dict=db_copy,
        sqlQuery=sql,
        failOnError=True,
        errMsg=ERR_DB_GET_SPACE % db_dict['name'],
        envDict={'ENGINE_PGPASS': PGPASS_FILE}
    )
    size = int(out[0]['pg_database_size'])
    size = size / pow(20,2) # Get size in MB
    return size


def performBackup(db_dict, backupPath, PGPASS_FILE):
    # Check abvailable space
    dbSize = getDbSize(db_dict, PGPASS_FILE)
    backupPathFree = getAvailableSpace(backupPath)
    doBackup = None
    proceed = None

    if (dbSize * 1.1) < backupPathFree:
        # allow upgrade, ask for backup
        msg = '{header}{cont}'.format(
            header=DB_BACKUP_HEADER,
            cont=DB_BACKUP_SHOW_CONTINUE,
        ).format(
            dbsize=dbSize,
            backup=backupPath,
            foldersize=backupPathFree,
        )
        if askYesNo(msg):
            proceed = DB_BACKUP_CONTINUE_WITH
            doBackup = True
        else:
            proceed = DB_BACKUP_CONTINUE_WITHOUT
            doBackup = False

    else:
        # ask to continue without backup, stop if no.
        msg = '{header}{stop}'.format(
            header=DB_BACKUP_HEADER,
            stop=DB_BACKUP_SHOW_STOP,
        ).format(
            dbsize=dbSize,
            backup=backupPath,
            foldersize=backupPathFree,
        )

        if askYesNo(msg):
            proceed = DB_BACKUP_CONTINUE_WITHOUT
            doBackup = False

    if not proceed or not askYesNo(
        proceed.format(
            db=db_dict['name']
        )
    ):
        raise UserWarning(
            'User decided to stop setup. Exiting'
        )

    return doBackup

@transactionDisplay("Backing up the DB")
def backupDB(backup_file, db_dict):
    """
    Backup postgres db
    Args:  file - a target file to backup to
           db_dict = DB connection object

    """
    logging.debug("%s DB Backup started", db_dict['name'])

    # Run backup
    cmd = [
        EXEC_PGDUMP,
        '-C',
        '-E',
        'UTF8',
        '--disable-dollar-quoting',
        '--disable-triggers',
        '--format=p',
        '-U', db_dict['username'],
        '-h', db_dict['host'],
        '-p', db_dict['port'],
        '-Fc',
        '-f', backup_file,
        db_dict['name'],
    ]
    execCmd(
        cmdList=cmd,
        failOnError=True,
        msg='Error during DB backup.',
    )
    logging.debug("%s DB Backup completed successfully", db_dict['name'])


def getUsernameId(username):
    return pwd.getpwnam(username)[2]


def getGroupId(groupName):
    return grp.getgrnam(groupName)[2]


def createTempPgpass(db_dict, mode='all'):

    fd, pgpass = tempfile.mkstemp(
        prefix='pgpass',
        suffix='.tmp',
    )
    os.close(fd)
    os.chmod(pgpass, 0o600)
    with open(pgpass, 'w') as f:
        f.write(
            (
                '# DB USER credentials.\n'
                '{host}:{port}:{database}:{user}:{password}\n'
            ).format(
                host=db_dict['host'],
                port=db_dict['port'],
                database='*' if mode == 'all' else db_dict['name'],
                user=db_dict['username'],
                password=db_dict['password'],
            ),
        )

    return pgpass


def generatePassword():
    return '%s%s' % (
        ''.join([random.choice(string.digits) for i in xrange(4)]),
        ''.join([random.choice(string.letters) for i in xrange(4)]),
    )


def createUser(user, password, option='', database=''):
    sql_query_set = [
        (
            '"DROP ROLE if exists {user};"'
        ),
        (
            '"CREATE ROLE {user} with '
            '{option} login encrypted password \'{password}\';"'
        ),
    ]
    for sql_query in sql_query_set:
        sql_command = [
            EXEC_PSQL,
            '-U', 'postgres',
            '-c',
            sql_query.format(
                user=user,
                option=option,
                password=password,
                database=database,
            ),
        ]
        if database is not '':
            sql_command.extend(
                [
                    '-d', database,
                ]
            )
        cmd = [
            EXEC_SU,
            '-l',
            'postgres',
            '-c',
            '{command}'.format(
                command=' '.join(sql_command),
            )
        ]

        execCmd(
            cmdList=cmd,
            failOnError=True
        )


def updateReadOnly(user, database):
    sql_query_set = [
        (
            '"GRANT CONNECT ON DATABASE {database} TO {user};"'
        ),
        (
            '"GRANT USAGE ON SCHEMA public TO {user};"'
        ),
        (
            '"alter user {user} '
            'set default_transaction_read_only to true;"'
        ),
    ]
    for sql_query in sql_query_set:
        sql_command = [
            EXEC_PSQL,
            '-U', 'postgres',
            '-d', database,
            '-c',
            sql_query.format(
                user=user,
                database=database,
            ),
        ]
        cmd = [
            EXEC_SU,
            '-l',
            'postgres',
            '-c',
            '{command}'.format(
                command=' '.join(sql_command),
            )
        ]

        execCmd(
            cmdList=cmd,
            failOnError=True
        )

        namespace_query = (
            '"SELECT \'GRANT SELECT ON \' || relname || \' '
            'TO {user};\' FROM pg_class JOIN pg_namespace '
            'ON pg_namespace.oid = pg_class.relnamespace '
            'WHERE nspname = \'public\' AND relkind IN (\'r\', \'v\');"'
        )
        sql_command = [
            EXEC_PSQL,
            '-U', 'postgres',
            '-d', database,
            '-c',
            namespace_query.format(
                user=user,
            ),
        ]
        cmd = [
            EXEC_SU,
            '-l',
            'postgres',
            '-c',
            '{command}'.format(
                command=' '.join(sql_command),
            )
        ]

        commands, rc = execCmd(
            cmdList=cmd,
            failOnError=True
        )

        commands = (line for line in commands.splitlines() if 'GRANT' in line)

        with open(READ_ONLY_UPDATE_SQLFILE, 'w') as ro:
            ro.write('\n'.join(commands))

        if os.path.exists(READ_ONLY_UPDATE_SQLFILE):
            command = [
                EXEC_PSQL,
                '-U', 'postgres',
                '-d', database,
                '-f', READ_ONLY_UPDATE_SQLFILE,
            ]
            cmd = [
                EXEC_SU,
                '-l',
                'postgres',
                '-c',
                '{command}'.format(
                    command=' '.join(command),
                )
            ]
            execCmd(
                cmdList=cmd,
                failOnError=True,
            )


def testLocalDb():
    sql_query_set = [
        (
            '"create database engine_test;"'
        ),
        (
            '"drop database engine_test;"'
        ),
    ]
    for sql_query in sql_query_set:
        sql_command = [
            EXEC_PSQL,
            '-U', 'postgres',
            '-c',
            sql_query,
        ]
        cmd = [
            EXEC_SU,
            '-l',
            'postgres',
            '-c',
            '{command}'.format(
                command=' '.join(sql_command),
            )
        ]

        execCmd(
            cmdList=cmd,
            failOnError=True
        )

    return True


def updatePgHba(database, user):
    content = []
    logging.debug('Updating pghba')
    with open(FILE_PG_HBA, 'r') as pghba:
        for line in pghba.read().splitlines():
            if user in line:
                return

            if 'engine          engine          0.0.0.0/0' in line:
                for address in ('0.0.0.0/0', '::0/0'):
                    content.append(
                        (
                            '{host:7} '
                            '{database:15} '
                            '{user:15} '
                            '{address:23} '
                            '{auth}'
                        ).format(
                            host='host',
                            user=user,
                            database='all',
                            address=address,
                            auth='md5',
                        )
                    )

            content.append(line)

    with open(FILE_PG_HBA, 'w') as pghba:
        pghba.write('\n'.join(content))
