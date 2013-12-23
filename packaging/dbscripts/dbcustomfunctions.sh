#!/bin/bash

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

set_defaults() {
    ME=$(basename $0)
    SERVERNAME="localhost"
    PORT="5432"
    DATABASE="ovirt_engine_history"
    USERNAME="engine_history"
    VERBOSE=false
    LOGFILE="$ME.log"
    DBOBJECT_OWNER="engine_history"
    NOMD5="false"
    MD5DIR="$(pwd)"
    LC_ALL="C"
    export LC_ALL

    if [ -n "${ENGINE_PGPASS}" ]; then
        export PGPASSFILE="${ENGINE_PGPASS}"
        unset PGPASSWORD
    else
        export PGPASSFILE="/etc/ovirt-engine/.pgpass"
        if [ ! -r "${PGPASSFILE}" ]; then
            export PGPASSFILE="${HOME}/.pgpass"
        fi
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
    printf "Creating views API 3.4...\n"
	execute_file "create_views_3_4.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
    printf "Creating ovirt engine reports views...\n"
    execute_file "create_reports_views.sql" ${DATABASE} ${SERVERNAME} ${PORT} > /dev/null
}

fn_db_set_dbobjects_ownership() {
    cmd="select c.relname \
         from   pg_class c join pg_roles r on r.oid = c.relowner join pg_namespace n on n.oid = c.relnamespace \
         where  c.relkind in ('r','v','S') \
         and    n.nspname = 'public' and r.rolname != '${DBOBJECT_OWNER}';"
    res=$(execute_command "${cmd}" engine ${SERVERNAME} ${PORT})
    if [ -n "${res}" ]; then
        cmd=""
        for tab in $(echo $res); do
            cmd=${cmd}"alter table $tab owner to ${DBOBJECT_OWNER}; "
        done
        if [ -n "${cmd}" ]; then
            echo -n "Changing ownership of objects in database '$DATABASE' to owner '$DBOBJECT_OWNER' ... "
            res=$(execute_command "${cmd}" engine ${SERVERNAME} ${PORT})
            if [ $? -eq 0 ]; then
                echo "completed successfully."
            else
                return 1
            fi
        fi
    fi
}

# Materilized views functions, override with empty implementation on DBs that not supporting that

install_materialized_views_func() {
    printf ""
}

drop_materialized_views() {
    printf ""
}

refresh_materialized_views() {
    printf ""
}
