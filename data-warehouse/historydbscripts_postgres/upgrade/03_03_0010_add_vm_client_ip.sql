select fn_db_add_column('vm_samples_history', 'vm_client_ip', 'varchar(255)');
select fn_db_add_column('statistics_vms_users_usage_hourly', 'vm_client_ip', 'varchar(255)');
select fn_db_add_column('statistics_vms_users_usage_daily', 'vm_client_ip', 'varchar(255)');
