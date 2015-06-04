-- Added vm Chached / Buffered memory in KB
select fn_db_add_column('vm_samples_history', 'memory_buffered_kb', 'integer');
select fn_db_add_column('vm_samples_history', 'memory_cached_kb', 'integer');
select fn_db_add_column('vm_hourly_history', 'memory_buffered_kb', 'integer');
select fn_db_add_column('vm_hourly_history', 'memory_cached_kb', 'integer');
select fn_db_add_column('vm_daily_history', 'memory_buffered_kb', 'integer');
select fn_db_add_column('vm_daily_history', 'memory_cached_kb', 'integer');

-- Added Max vm Chached / Buffered memory in KB to hourly and daily tables
select fn_db_add_column('vm_hourly_history', 'max_memory_buffered_kb', 'integer');
select fn_db_add_column('vm_hourly_history', 'max_memory_cached_kb', 'integer');
select fn_db_add_column('vm_daily_history', 'max_memory_buffered_kb', 'integer');
select fn_db_add_column('vm_daily_history', 'max_memory_cached_kb', 'integer');
