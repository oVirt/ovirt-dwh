#!/usr/bin/python
'''
common utils for rhev-dwh-setup
'''

import logging
import os
import traceback
import datetime
import re
from StringIO import StringIO
import subprocess
import shutil
from decorators import transactionDisplay
import tempfile

#text colors
RED = "\033[0;31m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
NO_COLOR = "\033[0m"
JBOSS_SERVICE_NAME = "ovirt-engine"

# CONST
EXEC_IP = "/sbin/ip"
FILE_PG_PASS="/etc/ovirt-engine/.pgpass"
PGPASS_FILE_USER_LINE = "DB USER credentials"
PGPASS_FILE_ADMIN_LINE = "DB ADMIN credentials"
FILE_ENGINE_CONFIG_BIN="/usr/bin/engine-config"

# ERRORS
# TODO: Move all errors here and make them consistent
ERR_EXP_GET_CFG_IPS = "Error: could not get list of available IP addresses on this host"
ERR_EXP_GET_CFG_IPS_CODES = "Error: failed to get list of IP addresses"
ERR_RC_CODE = "Error: return Code is not zero"
ERR_WRONG_PGPASS_VALUE = "Error: unknown value type '%s' was requested"
ERR_PGPASS_VALUE_NOT_FOUND = "Error: requested value '%s' was not found \
in %s. Check oVirt Engine installation and that wildcards '*' are not used."

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

    def delParams(self, paramsDict):
        pass

def askYesNo(question=None):
    '''
    provides an interface that prompts the user
    to answer "yes/no" to a given question
    '''
    message = StringIO()
    ask_string = "%s? (yes|no): " % question
    logging.debug("asking user: %s" % ask_string)
    message.write(ask_string)
    message.seek(0)
    raw_answer = raw_input(message.read())
    logging.debug("user answered: %s"%(raw_answer))
    answer = raw_answer.lower()
    if answer == "yes" or answer == "y":
        return True
    elif answer == "no" or answer == "n":
        return False
    else:
        return askYesNo(question)

def execSqlCmd(db_dict, sql_query, fail_on_error=False, err_msg="Failed running sql query"):
    logging.debug("running sql query on host: %s, port: %s, db: %s, user: %s, query: \'%s\'." %
                  (db_dict["host"],
                   db_dict["port"],
                   db_dict["name"],
                   db_dict["username"],
                   sql_query))
    cmd = [
        "/usr/bin/psql",
        "--pset=tuples_only=on",
        "--set",
        "ON_ERROR_STOP=1",
        "--dbname", db_dict["name"],
        "--host", db_dict["host"],
        "--port", db_dict["port"],
        "--username", db_dict["username"],
        "-c", sql_query,
    ]
    return execCmd(cmdList=cmd, failOnError=fail_on_error, msg=err_msg)

def isJbossUp():
    '''
    checks if jboss-as is active
    '''
    logging.debug("checking the status of jboss-as")
    cmd = ["service", JBOSS_SERVICE_NAME, "status"]
    output, rc = execCmd(cmdList=cmd, msg="Failed while checking for jboss-as service status")
    if " is running" in output:
        return True
    else:
        return False

def stopJboss():
    '''
    stops the jboss-as service
    '''
    logging.debug("checking jboss-as service")
    if isJbossUp():
        logging.debug("jboss-as is up and running")
        print "In order to proceed the installer must stop the JBoss service"
        answer = askYesNo("Would you like to stop the JBoss service")
        if answer:
            stopJbossService()
        else:
            logging.debug("User chose not to stop jboss")
            return False
    return True

@transactionDisplay("Stopping Jboss")
def stopJbossService():
    logging.debug("Stopping jboss")
    cmd = ["service", JBOSS_SERVICE_NAME, "stop"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to stop the jboss-as service")

def startJboss():
    '''
    starts the jboss-as service
    '''
    if not isJbossUp():
        startJbossService()
    else:
        logging.debug("jobss is up. nothing to start")

@transactionDisplay("Starting Jboss")
def startJbossService():
    logging.debug("Starting jboss")
    cmd = ["service", JBOSS_SERVICE_NAME, "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the jboss-as service")

def isPostgresUp():
    '''
    checks if the postgresql service is up and running
    '''
    logging.debug("checking the status of postgresql")
    cmd = ["service", "postgresql", "status"]
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

@transactionDisplay("Starting PostgresSql")
def startPostgresService():
    logging.debug("starting postgresql")
    cmd = ["service", "postgresql", "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the postgresql service")

def stopEtl():
    """
    stop the ovirt-engine-dwhd service
    """
    logging.debug("Stopping ovirt-engine-dwhd")
    cmd = ["service", "ovirt-engine-dwhd", "stop"]
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
    cmd = ["service", "ovirt-engine-dwhd", "start"]
    execCmd(cmdList=cmd, failOnError=True, msg="Failed while trying to start the ovirt-engine-dwhd service")

def isEtlUp():
    '''
    checks if ovirt-engine-dwhd is active
    '''
    logging.debug("checking the status of ovirt-engine-dwhd")
    cmd = ["service", "ovirt-engine-dwhd", "status"]
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
    minorVersion= found.group(2)
    release = found.group(3)

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
    Retrieve Admin user from .pgpass file on the system.
    Use default settings if file is not found.
    """
    return getDbConfig("admin")

def getDbHostName():
    """
    Retrieve DB Host name from .pgpass file on the system.
    Use default settings if file is not found, or '*' was used.
    """

    return getDbConfig("host")

def getDbPort():
    """
    Retrieve DB port number from .pgpass file on the system.
    """
    return getDbConfig("port")

def getDbConfig(dbconf_param):
    """
    Generic function to retrieve values from admin line in .pgpass
    """
    # 'user' and 'admin' are the same fields, just different lines
    # and for different cases
    field = {'user' : 3, 'admin' : 3, 'host' : 0, 'port' : 1}
    if dbconf_param not in field.keys():
        raise Exception(ERR_WRONG_PGPASS_VALUE % dbconf_param)

    inDbAdminSection = False
    inDbUserSection = False
    if (os.path.exists(FILE_PG_PASS)):
        logging.debug("found existing pgpass file, fetching DB %s value" % dbconf_param)
        with open (FILE_PG_PASS) as pgPassFile:
            for line in pgPassFile:

                # find the line with "DB ADMIN"
                if PGPASS_FILE_ADMIN_LINE in line:
                    inDbAdminSection = True
                    continue

                if inDbAdminSection and dbconf_param == "admin" and \
                   not line.startswith("#"):
                    # Means we're on DB ADMIN line, as it's for all DBs
                    dbcreds = line.split(":", 4)
                    return dbcreds[field[dbconf_param]]

                # find the line with "DB USER"
                if PGPASS_FILE_USER_LINE in line:
                    inDbUserSection = True
                    continue

                # fetch the values
                if inDbUserSection:
                    # Means we're on DB USER line, as it's for all DBs
                    dbcreds = line.split(":", 4)
                    return dbcreds[field[dbconf_param]]

    raise Exception(ERR_PGPASS_VALUE_NOT_FOUND % (dbconf_param, FILE_PG_PASS))

def getPassFromFile(username):
    '''
    get the password for specified user
    from /root/.pgpass
    '''
    logging.debug("getting DB password for %s" % username)
    with open(FILE_PG_PASS, "r") as fd:
        for line in fd.readlines():
            if line.startswith("#"):
                continue
            # Max 4 splits, so if password includes ':' character, it
            # would still work fine.
            list = line.split(":", 4)
            if list[3] == username:
                logging.debug("found password for username %s" % username)
                return list[4].rstrip('\n')

    # If no pass was found, return None
    return None

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

#TODO: Move all execution commands to execCmd
def execCmd(cmdList, cwd=None, failOnError=False, msg=ERR_RC_CODE, maskList=[], useShell=False, usePipeFiles=False, envDict={}):
    """
    Run external shell command with 'shell=false'
    receives a list of arguments for command line execution
    """
    # All items in the list needs to be strings, otherwise the subprocess will fail
    cmd = [str(item) for item in cmdList]

    logging.debug("Executing command --> '%s'"%(cmd))

    stdErrFD = subprocess.PIPE
    stdOutFD = subprocess.PIPE
    stdInFD = subprocess.PIPE

    if usePipeFiles:
        (stdErrFD, stdErrFile) = tempfile.mkstemp(dir="/tmp")
        (stdOutFD, stdOutFile) = tempfile.mkstemp(dir="/tmp")
        (stdInFD, stdInFile) = tempfile.mkstemp(dir="/tmp")

    # Update os.environ with env if provided
    env = os.environ.copy()
    if not "PGPASSFILE" in env.keys():
        env["PGPASSFILE"] = FILE_PG_PASS
    env.update(envDict)

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
