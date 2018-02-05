-- Update vm_interface_* statistics table history_id to bigint

SELECT fn_db_change_column_type('vm_interface_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_interface_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_interface_samples_history', 'history_id', 'integer', 'bigint');
