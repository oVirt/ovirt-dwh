#!/bin/bash
#

LOGFILE="/var/log/ovirt-engine/ovirt-engine-dwhd.log"
ETL_HOME=/usr/share/ovirt-engine-dwh/etl
JAVA_DIR=/usr/share/java
CP=$ETL_HOME:$ETL_HOME/historyETLProcedure-3.0.0.jar:$ETL_HOME/lib/advancedPersistentLookupLib-1.0.jar:$ETL_HOME/lib/talendRoutines-5.0.1.r74687.jar:$ETL_HOME/lib/xml-apis-1.0.b2.jar:$ETL_HOME/lib/trove.jar:$ETL_HOME/lib/jboss-serialization.jar:$JAVA_DIR/dom4j.jar:$JAVA_DIR/commons-collections.jar:$JAVA_DIR/log4j.jar:$JAVA_DIR/postgresql-jdbc.jar

exec java -Xms256M -Xmx1024M -cp $CP ovirt_engine_dwh.historyetl_3_0.HistoryETL --context=Default $* >> $LOGFILE 2>&1 &
echo $! >$ETL_PID
