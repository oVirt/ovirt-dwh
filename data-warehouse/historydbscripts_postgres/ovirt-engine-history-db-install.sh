#!/bin/bash
#
# Copyright 2009-2011 Red Hat, Inc. All rights reserved.
# Use is subject to license terms.
#
# Description:      Installs and configs postgres db for ovirt_engine_history
#
# note: this script should be run as root in order to have the permissions to create the nessesary files on the fs.
#
# internal script - run only by ovirt-engine-dwh-setup.py after creating CA
#
# this script will create the ovirt_engine_history db
# the file /root/.pgpass must exsists (created by ovirt-setup) after this script finish,
# in order to access the db

# GLOBALS
HOST=`/bin/hostname`
SCRIPT_NAME="ovirt-history-db-install"
CUR_DATE=`date +"%Y_%m_%d_%H_%M_%S"`

#postgresql data dir
ENGINE_PGPASS=${ENGINE_PGPASS:-/etc/ovirt-engine/.pgpass}
PGDATA=/var/lib/pgsql/data

#location of ovirt db scripts
OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR=/usr/share/ovirt-engine-dwh/db-scripts
OVIRT_ENGINE_HISTORY_DB_CREATE_SCRIPT=create_db.sh

#postresql service
PGSQL=postgresql
DB_ADMIN=postgres
DB_USER=postgres
DB_PORT=5432
DB_HOST="localhost"
TABLE_NAME=vm_configuration
DB_NAME=ovirt_engine_history
LOCAL_DB_SET=1

#auth security file path
PG_HBA_FILE=/var/lib/pgsql/data/pg_hba.conf

#uuid generate sql
UUID_SQL=/usr/share/pgsql/contrib/uuid-ossp.sql
LOG_PATH=/var/log/ovirt-engine
USER=`/usr/bin/whoami`

usage() {
    printf "Usage: ${ME} [-h] [-s SERVERNAME [-p PORT]] [-d DATABASE] [-u USERNAME] [-r 'remote'] -l LOGFILE [-L LOGDIR]\n"
    printf "\n"
    printf "\t-s SERVERNAME - The database servername for the database  (def. ${DB_HOST})\n"
    printf "\t-p PORT       - The database port for the database        (def. ${DB_PORT})\n"
    printf "\t-d DATABASE   - The database name                         (def. ${DB_NAME})\n"
    printf "\t-u USERNAME   - The admin username for the database.\n    (def. ${DB_ADMIN})\n"
    printf "\t-l LOGFILE    - The logfile for capturing output          (def. ${LOGFILE})\n"
    printf "\t-r REMOTE_INSTALL - The flag for peforming remote install (def. ${REMOTE_INSTALL})\n"
    printf "\t-h            - This help text.\n"
    printf "\n"

    exit 0
}

#EXTERNAL ARGS
while getopts :s:p:d:u:w:l:L:r:h option; do
    case $option in
        s) DB_HOST=$OPTARG;;
        p) DB_PORT=$OPTARG;;
        d) DB_NAME=$OPTARG;;
        u) DB_ADMIN=$OPTARG;;
        l) LOG_FILE=$OPTARG;;
        L) LOG_PATH=$OPTARG;;
        r) REMOTE_INSTALL=$OPTARG;;
        h) usage;;
    esac
done


# COMMANDS
CHKCONFIG=/sbin/chkconfig
COPY=/bin/cp
SED=/bin/sed
SHELL=/bin/sh
PSQL_BIN=/usr/bin/psql

# Update PSQL BIN to include host and port values
PSQL="${PSQL_BIN} -h $DB_HOST -p $DB_PORT"

if [[ "x${REMOTE_INSTALL}" == "xremote" ]]
then
    LOCAL_DB_SET=0
fi

verifyArgs()
{
    #if we dont have mandatory args, exit with 1
    if [[ "x${LOG_FILE}" == "x" ]]
    then
        echo "$SCRIPT_NAME must get log filename as argument 1"
        exit 1
    fi
}

verifyRunPermissions()
{
    if [[ ! $USER == "root" ]]
    then
        echo "user $USER doesn't have permissions to run the script, please use root only."
        exit 1
    fi
}

_verifyRC()
{
    RC=$1
    STR=$2
    if [[ ! $RC -eq 0 ]]
    then
        echo "$2"
        exit 1
    fi
}

initLogFile()
{
    if [[ ! -d $LOG_PATH ]]
    then
        mkdir  $LOG_PATH > /dev/null
    fi
     _verifyRC $? "error, failed creating log dir $LOG_PATH"

    LOG_FILE="$LOG_PATH/$LOG_FILE"
    echo "#ovirt engine history db installer log file on $HOST" > $LOG_FILE
}


initPgsqlDB()
{
    echo "[$SCRIPT_NAME] init postgres db." >> $LOG_FILE
    #verify is service postgres initdb has run already
    if [ -e "$PGDATA/PG_VERSION" ]
    then
        echo "[$SCRIPT_NAME] psgql db already been initialized." >> $LOG_FILE
    else
        service $PGSQL initdb >> $LOG_FILE 2>&1
        _verifyRC $? "error, failed initializing postgresql db"
        turnPgsqlOnStartup
        startPgsqlService postgres postgres
    fi
}

startPgsqlService()
{
    USER=$1
    DB=$2
    echo "[$SCRIPT_NAME] stop postgres service." >> $LOG_FILE
    service $PGSQL stop >> $LOG_FILE 2>&1

    echo "[$SCRIPT_NAME] starting postgres service." >> $LOG_FILE
    service $PGSQL start >> $LOG_FILE 2>&1
    _verifyRC $? "failed starting postgresql service"

    #verify that the postgres service is up before continuing
    SERVICE_UP=0
    for i in {1..20}
    do
       echo "[$SCRIPT_NAME] validating that postgresql service is running...retry $i" >> $LOG_FILE
       PGPASSFILE="${ENGINE_PGPASS}" $PSQL -U $USER -d $DB -w -c "select 1">> $LOG_FILE 2>&1
       if [[ $? == 0 ]]
       then
            SERVICE_UP=1
            break
       fi
       sleep 1
    done

    if [[ $SERVICE_UP != 1 ]]
    then
        echo "[$SCRIPT_NAME] failed loading postgres service - timeout expired." >> $LOG_FILE
        exit 1
    fi
}

#change auth from default ident to trust
#TODO: Handle more auth types in the future
changePgAuthScheme()
{
    OLD=$1
    NEW=$2
    OLD_OPTIONAL=$3
    echo "[$SCRIPT_NAME] changing authentication scheme from $OLD to $NEW." >> $LOG_FILE
    #backup original hba file
    BACKUP_HBA_FILE=$PG_HBA_FILE.orig
    if [ -r $PG_HBA_FILE ]
    then
        $COPY $PG_HBA_FILE $BACKUP_HBA_FILE
        _verifyRC $? "error, failed backing up auth file $PG_HBA_FILE"
    else
       echo "[$SCRIPT_NAME] can't find pgsql auto file $PG_HBA_FILE." >> $LOG_FILE
       exit 1
    fi

    #if we dont have optional old, use old
        if [[ "x${OLD_OPTIONAL}" == "x" ]]
        then
               OLD_OPTIONAL=$OLD
        fi

    #sed will replace any OLD with NEW but will ignore comment and empty lines
    eval "$SED -i -e '/^[[:space:]]*#/!s/$OLD/$NEW/g' -e '/^[[:space:]]*#/!s/$OLD_OPTIONAL/$NEW/g' $PG_HBA_FILE" >> $LOG_FILE 2>&1
    _verifyRC $? "error, failed updating hba auth file $PG_HBA_FILE"
}

#TODO: handle remote DB Installation
#TODO: handle history DB Installation
createDB()
{
    echo "[$SCRIPT_NAME] creating $DB_NAME db on postgres." >> $LOG_FILE
    if [[ -d "$OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR" && -e "$OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR/$OVIRT_ENGINE_HISTORY_DB_CREATE_SCRIPT" ]]
    then
        pushd $OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR >> $LOG_FILE
        #TODO: to we need to verify if the db was already created? (we can create a new file and check if exists..)
        CREATE_DB="$OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR/$OVIRT_ENGINE_HISTORY_DB_CREATE_SCRIPT"
        PGPASSFILE="${ENGINE_PGPASS}" "${CREATE_DB}" -s $DB_HOST -p $DB_PORT -u $DB_ADMIN >> $LOG_FILE 2>&1
        _verifyRC $? "error, failed creating ovirt engine history db"
        popd >> $LOG_FILE

    else
        echo "[$SCRIPT_NAME] error, can't find create_db script at $OVIRT_ENGINE_HISTORY_DB_SCRIPTS_DIR/$OVIRT_ENGINE_HISTORY_DB_CREATE_SCRIPT"
        exit 1
    fi
}

checkIfDBExists()
{
    echo "[$SCRIPT_NAME] checking if $DB_NAME db exists already.." >> $LOG_FILE
    PGPASSFILE="${ENGINE_PGPASS}" $PSQL -U $DB_ADMIN -d $DB_NAME -c "select 1">> $LOG_FILE 2>&1
    if [[ $? -eq 0 ]]
    then
        echo "[$SCRIPT_NAME] $DB_NAME db already exists on $DB_HOST." >> $LOG_FILE
        echo " [$SCRIPT_NAME] verifying $TABLE_NAME table exists..." >> $LOG_FILE
        RES=`echo "SELECT count(*) FROM pg_tables WHERE tablename='$TABLE_NAME'" | PGPASSFILE="${ENGINE_PGPASS}" $PSQL -U $DB_ADMIN -d $DB_NAME -t`
        if [[ $RES -eq 1 ]]
        then
            echo "[$SCRIPT_NAME] $TABLE_NAME table exists in $DB_NAME" >> $LOG_FILE
            #rc 1 means - no actions is needed
            return 1
        else
            echo "[$SCRIPT_NAME] $TABLE_NAME table doesn't exists in $DB_NAME" >> $LOG_FILE
            #rc 2 means - something is wrong, db exists but table doesnt!
            return 2
        fi
    else
        echo "[$SCRIPT_NAME] $DB_NAME not installed." >> $LOG_FILE
        return 0
    fi
}

turnPgsqlOnStartup()
{
    #turn on the postgres service on startup
    $CHKCONFIG $PGSQL on >> $LOG_FILE 2>&1
    _verifyRC $? "failed adding postgresql to startup scripts"
}

# Main

verifyArgs
verifyRunPermissions
initLogFile
# The following should only run during local installation
if [[ $LOCAL_DB_SET -eq 1 ]]
then
    initPgsqlDB
fi

checkIfDBExists

#get return value from checkIfDBExists function
DB_EXISTS=$?
if [[ $DB_EXISTS -eq 0 ]]
then
    createDB
    if [[ $LOCAL_DB_SET -eq 1 ]]
    then
        startPgsqlService $DB_ADMIN ovirt_engine_history
    fi
elif [[ $DB_EXISTS -eq 2 ]]
then
   echo "[$SCRIPT_NAME] error, $TABLE_NAME doesnt exists on DB $DB_NAME" >> $LOG_FILE
   exit 1
fi


echo "[$SCRIPT_NAME] finished installing postgres db on $DB_HOST." >> $LOG_FILE
exit 0
