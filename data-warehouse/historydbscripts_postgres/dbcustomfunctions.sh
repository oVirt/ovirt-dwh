#!/bin/bash

insert_initial_data() {
    printf "Inserting Period Table Values ...\n"
    execute_file "insert_period_table_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting Timekeeping Values  ...\n"
    execute_file "insert_timekeeping_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting ENUM Values ...\n"
    execute_file "insert_enum_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting Calendar Table's Values ...\n"
    execute_file "insert_calendar_table_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
}

set_defaults() {
    ME=$(basename $0)
    SERVERNAME="localhost"
    PORT=5432
    DATABASE="ovirt_engine_history"
    USERNAME="postgres"
    VERBOSE=false
    LOGFILE="$ME.log"
    export PGPASSFILE="/etc/ovirt-engine/.pgpass"
}

#refreshes views
refresh_views() {
    printf "Creating views API 3.0...\n"
    execute_file "create_views_3_0.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Creating views API 3.1...\n"
    execute_file "create_views_3_1.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Creating views API 3.2...\n"
    execute_file "create_views_3_2.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Creating views API 3.3...\n"
    execute_file "create_views_3_3.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Creating ovirt engine reports views...\n"
    execute_file "create_reports_views.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
}
