select fn_db_add_column('vm_samples_history', 'user_logged_in_to_guest', 'BOOLEAN');
select fn_db_add_column('statistics_vms_users_usage_hourly', 'user_logged_in_to_guest', 'BOOLEAN');
select fn_db_add_column('statistics_vms_users_usage_daily', 'user_logged_in_to_guest', 'BOOLEAN');
