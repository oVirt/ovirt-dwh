-- Update vm buffered and cached memory to bigint

SELECT fn_db_change_column_type('vm_samples_history', 'memory_buffered_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_samples_history', 'memory_cached_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_hourly_history', 'memory_buffered_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_hourly_history', 'memory_cached_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_daily_history', 'memory_buffered_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_daily_history', 'memory_cached_kb', 'integer', 'bigint');

SELECT fn_db_change_column_type('vm_hourly_history', 'max_memory_buffered_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_hourly_history', 'max_memory_cached_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_daily_history', 'max_memory_buffered_kb', 'integer', 'bigint');
SELECT fn_db_change_column_type('vm_daily_history', 'max_memory_cached_kb', 'integer', 'bigint');
