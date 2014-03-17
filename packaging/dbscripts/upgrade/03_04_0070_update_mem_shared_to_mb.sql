-- add ksm_shared_memory_mb to host_samples_history table
SELECT fn_db_add_column('host_samples_history', 'ksm_shared_memory_mb', 'bigint');

--delete ksm_shared_memory_percent column from host_samples_history table
SELECT fn_db_drop_column('host_samples_history', 'ksm_shared_memory_percent');

-- add ksm_shared_memory_mb to host_hourly_history table
SELECT fn_db_add_column('host_hourly_history', 'ksm_shared_memory_mb', 'bigint');
SELECT fn_db_add_column('host_hourly_history', 'max_ksm_shared_memory_mb', 'bigint');

--delete ksm_shared_memory_percent column from host_hourly_history table
SELECT fn_db_drop_column('host_hourly_history', 'ksm_shared_memory_percent');
SELECT fn_db_drop_column('host_hourly_history', 'max_ksm_shared_memory_percent');

-- add ksm_shared_memory_mb to host_daily_history table
SELECT fn_db_add_column('host_daily_history', 'ksm_shared_memory_mb', 'bigint');
SELECT fn_db_add_column('host_daily_history', 'max_ksm_shared_memory_mb', 'bigint');

--delete ksm_shared_memory_percent column from host_samples_history table
SELECT fn_db_drop_column('host_daily_history', 'ksm_shared_memory_percent');
SELECT fn_db_drop_column('host_daily_history', 'max_ksm_shared_memory_percent');
