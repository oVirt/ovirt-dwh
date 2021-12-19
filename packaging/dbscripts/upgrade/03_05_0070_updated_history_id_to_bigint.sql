-- Update statistics table history_id to bigint

SELECT fn_db_change_column_type('datacenter_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('datacenter_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('datacenter_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_interface_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_interface_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('host_interface_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('statistics_vms_users_usage_daily', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('statistics_vms_users_usage_hourly', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('storage_domain_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('storage_domain_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('storage_domain_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disk_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disk_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disk_samples_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disks_usage_daily_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disks_usage_hourly_history', 'history_id', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_disks_usage_samples_history', 'history_id', 'integer', 'bigint');
