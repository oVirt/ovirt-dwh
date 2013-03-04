#!/bin/bash -x
#

ENGINE_DEFAULTS="${ENGINE_DEFAULTS:-/usr/share/ovirt-engine/conf/engine.conf.defaults}"
ENGINE_VARS="${ENGINE_VARS:-/etc/ovirt-engine/engine.conf}"
for f in "${ENGINE_DEFAULTS}" "${ENGINE_VARS}" $(find "${ENGINE_VARS}.d" -name '*.conf' | sort); do
    [ -r "${f}" ] && . "${f}"
done

LOGFILE="/var/log/ovirt-engine/ovirt-engine-dwhd.log"
ETL_HOME=/usr/share/ovirt-engine-dwh/etl
JAVA_DIR=/usr/share/java
RUN_PROPERTIES="-Xms256M -Xmx1024M"
CP=$ETL_HOME:$JAVA_DIR/ovirt-engine-dwh/historyETLProcedure.jar:$JAVA_DIR/ovirt-engine-dwh/advancedPersistentLookupLib.jar:$JAVA_DIR/ovirt-engine-dwh/talendRoutines.jar:$JAVA_DIR/dom4j.jar:$JAVA_DIR/commons-collections.jar:$JAVA_DIR/log4j.jar:$JAVA_DIR/postgresql-jdbc.jar

exec ${JAVA_HOME}/bin/java $RUN_PROPERTIES -cp $CP ovirt_engine_dwh.historyetl_3_2.HistoryETL --context=Default $* >> $LOGFILE 2>&1 &
echo $! >$ETL_PID
