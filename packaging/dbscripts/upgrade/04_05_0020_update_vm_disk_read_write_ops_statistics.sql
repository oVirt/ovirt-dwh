-- Change vm disk IOPS statistics names
select fn_db_rename_column('vm_disk_samples_history', 'read_ops_per_second', 'read_ops_total_count');
select fn_db_rename_column('vm_disk_samples_history', 'write_ops_per_second', 'write_ops_total_count');
select fn_db_rename_column('vm_disk_hourly_history', 'read_ops_per_second', 'read_ops_total_count');
select fn_db_rename_column('vm_disk_hourly_history', 'write_ops_per_second', 'write_ops_total_count');
select fn_db_rename_column('vm_disk_daily_history', 'read_ops_per_second', 'read_ops_total_count');
select fn_db_rename_column('vm_disk_daily_history', 'write_ops_per_second', 'write_ops_total_count');
-- Change vm disk IOPS statistics types
select fn_db_change_column_type('vm_disk_samples_history', 'read_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
select fn_db_change_column_type('vm_disk_samples_history', 'write_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
select fn_db_change_column_type('vm_disk_hourly_history', 'read_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
select fn_db_change_column_type('vm_disk_hourly_history', 'write_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
select fn_db_change_column_type('vm_disk_daily_history', 'read_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
select fn_db_change_column_type('vm_disk_daily_history', 'write_ops_total_count', 'bigint', 'NUMERIC(20, 0)');
-- Drop max vm disk IOPS per second
select fn_db_drop_column('vm_disk_hourly_history', 'max_read_ops_per_second');
select fn_db_drop_column('vm_disk_hourly_history', 'max_write_ops_per_second');
select fn_db_drop_column('vm_disk_daily_history', 'max_read_ops_per_second');
select fn_db_drop_column('vm_disk_daily_history', 'max_write_ops_per_second');
