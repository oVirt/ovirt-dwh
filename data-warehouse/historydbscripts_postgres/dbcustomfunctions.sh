#!/bin/bash

set_defaults() {
    ME=$(basename $0)
    SERVERNAME="localhost"
    PORT=5432
    DATABASE="ovirt_engine_history"
    USERNAME="postgres"
    VERBOSE=false
    LOGFILE="$ME.log"
    if [ -n "${ENGINE_PGPASS}"  ]; then
        export PGPASSFILE="${ENGINE_PGPASS}"
    else
        export PGPASSFILE="/etc/ovirt-engine/.pgpass"
    fi
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

insert_initial_data() {
    printf "Inserting data  ...\n"
    execute_file "insert_data.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting Timekeeping Values  ...\n"
    execute_file "insert_timekeeping_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting ENUM Values ...\n"
    execute_file "insert_enum_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Inserting Calendar Table's Values ...\n"
    execute_file "insert_calendar_table_values.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
}
