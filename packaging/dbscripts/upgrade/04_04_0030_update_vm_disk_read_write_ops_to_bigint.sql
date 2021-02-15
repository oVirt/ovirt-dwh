-- Change vm disk IOPS per second
select fn_db_change_column_type('vm_disk_samples_history', 'read_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_samples_history', 'write_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_hourly_history', 'read_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_hourly_history', 'write_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_daily_history', 'read_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_daily_history', 'write_ops_per_second', 'integer', 'bigint');
-- Change Max vm disk IOPS per second to hourly and daily tables
select fn_db_change_column_type('vm_disk_hourly_history', 'max_read_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_hourly_history', 'max_write_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_daily_history', 'max_read_ops_per_second', 'integer', 'bigint');
select fn_db_change_column_type('vm_disk_daily_history', 'max_write_ops_per_second', 'integer', 'bigint');