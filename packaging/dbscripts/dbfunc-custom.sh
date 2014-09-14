
. "${DBFUNC_COMMON_DBSCRIPTS_DIR}/dbfunc-common.sh"

DBFUNC_DB_USER="${DBFUNC_DB_USER:-ovirt_engine_history}"
DBFUNC_DB_DATABASE="${DBFUNC_DB_DATABASE:-ovirt_engine_history}"

DBFUNC_CUSTOM_CLEAN_TASKS=

dbfunc_common_hook_init_insert_data() {
	echo "Inserting data..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_data.sql" > /dev/null
	echo "Inserting Timekeeping Values..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_timekeeping_values.sql" > /dev/null
	echo "Inserting ENUM Values..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_enum_values.sql" > /dev/null
	echo "Inserting Calendar Table's Values..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_calendar_table_values.sql" > /dev/null
}

dbfunc_common_hook_views_refresh() {
	echo "Creating views API 3.0..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_0.sql" > /dev/null
	echo "Creating views API 3.1..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_1.sql" > /dev/null
	echo "Creating views API 3.2..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_2.sql" > /dev/null
	echo "Creating views API 3.3..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_3.sql" > /dev/null
	echo "Creating views API 3.4..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_4.sql" > /dev/null
	echo "Creating views API 3.5..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_5.sql" > /dev/null
	echo "Creating views API 3.6..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_6.sql" > /dev/null
	echo "Creating ovirt engine reports views..."
	dbfunc_psql_die --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_reports_views.sql" > /dev/null
}
