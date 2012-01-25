#!/bin/bash

insert_initial_data() {
	printf "Inserting Period Table Values ...\n"
	execute_file "insert_period_table_values.sql" ${DATABASE} > /dev/null
	printf "Inserting Timekeeping Values  ...\n"
	execute_file "insert_timekeeping_values.sql" ${DATABASE} > /dev/null
	printf "Inserting ENUM Values ...\n"
	execute_file "insert_enum_values.sql" ${DATABASE} > /dev/null
	printf "Inserting Calendar Table's Values ...\n"
	execute_file "insert_calendar_table_values.sql" ${DATABASE} > /dev/null
}

set_defaults() {
    ME=$(basename $0)
    SERVERNAME="127.0.0.1"
    DATABASE="ovirt_history"
    USERNAME="postgres"
    VERBOSE=false
    LOGFILE="$ME.log"
}

