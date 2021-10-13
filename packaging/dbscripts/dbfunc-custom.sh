
. "${DBFUNC_COMMON_DBSCRIPTS_DIR}/dbfunc-common.sh"

DBFUNC_DB_USER="${DBFUNC_DB_USER:-ovirt_engine_history}"
DBFUNC_DB_DATABASE="${DBFUNC_DB_DATABASE:-ovirt_engine_history}"

DBFUNC_CUSTOM_CLEAN_TASKS=

dbfunc_common_hook_init_insert_data() {
	dbfunc_output "Inserting data..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_data.sql" > /dev/null
	dbfunc_output "Inserting Timekeeping Values..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_timekeeping_values.sql" > /dev/null
	dbfunc_output "Inserting ENUM Values..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_enum_values.sql" > /dev/null
	dbfunc_output "Inserting Calendar Table's Values..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/insert_calendar_table_values.sql" > /dev/null
}

dbfunc_common_hook_views_refresh() {
	dbfunc_output "Creating views API 3.6..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_3_6.sql" > /dev/null
	dbfunc_output "Creating views API 4.0..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_0.sql" > /dev/null
	dbfunc_output "Creating views API 4.1..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_1.sql" > /dev/null
	dbfunc_output "Creating views API 4.2..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_2.sql" > /dev/null
	dbfunc_output "Creating views API 4.3..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_3.sql" > /dev/null
	dbfunc_output "Creating views API 4.4..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_4.sql" > /dev/null
	dbfunc_output "Creating views API 4.5..."
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_views_4_5.sql" > /dev/null
	dbfunc_psql_die_v --file="${DBFUNC_COMMON_DBSCRIPTS_DIR}/create_reports_views.sql" > /dev/null
}
