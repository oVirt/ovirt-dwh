#!/bin/bash
#

LOGFILE="/var/log/ovirt/ovirt-etl.log"
ETL_HOME=/usr/share/ovirt-dwh/etl
CP=$ETL_HOME:$ETL_HOME/historyETLProcedure-3.0.0.jar:$ETL_HOME/lib/advancedPersistentLookupLib-1.0.jar:$ETL_HOME/lib/commons-collections.jar:$ETL_HOME/lib/jboss-serialization.jar:$ETL_HOME/lib/log4j.jar:$ETL_HOME/lib/postgresql-jdbc.jar:$ETL_HOME/lib/trove.jar:$ETL_HOME/lib/dom4j.jar:$ETL_HOME/lib/talendRoutines-5.0.1.r74687.jar:$ETL_HOME/lib/xml-apis-1.0.b2.jar

exec java -Xms256M -Xmx1024M -cp $CP ovirt_dwh.historyetl_3_0.HistoryETL --context=Default $* >> $LOGFILE 2>&1 &
echo $! >$ETL_PID
