select fn_db_add_column('host_interface_samples_history', 'received_total_byte', 'bigint');
select fn_db_add_column('host_interface_samples_history', 'transmitted_total_byte', 'bigint');
select fn_db_add_column('vm_interface_samples_history', 'received_total_byte', 'bigint');
select fn_db_add_column('vm_interface_samples_history', 'transmitted_total_byte', 'bigint');

select fn_db_add_column('host_interface_hourly_history', 'received_total_byte', 'bigint');
select fn_db_add_column('host_interface_hourly_history', 'transmitted_total_byte', 'bigint');
select fn_db_add_column('vm_interface_hourly_history', 'received_total_byte', 'bigint');
select fn_db_add_column('vm_interface_hourly_history', 'transmitted_total_byte', 'bigint');

select fn_db_add_column('host_interface_daily_history', 'received_total_byte', 'bigint');
select fn_db_add_column('host_interface_daily_history', 'transmitted_total_byte', 'bigint');
select fn_db_add_column('vm_interface_daily_history', 'received_total_byte', 'bigint');
select fn_db_add_column('vm_interface_daily_history', 'transmitted_total_byte', 'bigint');
