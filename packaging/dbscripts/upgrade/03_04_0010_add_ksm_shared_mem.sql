select fn_db_add_column('host_samples_history', 'ksm_shared_memory_percent', 'smallint');
select fn_db_add_column('host_hourly_history', 'ksm_shared_memory_percent', 'smallint');
select fn_db_add_column('host_hourly_history', 'max_ksm_shared_memory_percent', 'smallint');
select fn_db_add_column('host_daily_history', 'ksm_shared_memory_percent', 'smallint');
select fn_db_add_column('host_daily_history', 'max_ksm_shared_memory_percent', 'smallint');
