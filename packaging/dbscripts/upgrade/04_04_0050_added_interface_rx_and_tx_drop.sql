-- Added host interface drop
select fn_db_add_column('host_interface_samples_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('host_interface_samples_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('host_interface_hourly_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('host_interface_hourly_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('host_interface_daily_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('host_interface_daily_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');
-- Added vm interface drop
select fn_db_add_column('vm_interface_samples_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('vm_interface_samples_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('vm_interface_hourly_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('vm_interface_hourly_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('vm_interface_daily_history', 'received_dropped_total_packets', 'DECIMAL(18,4)');
select fn_db_add_column('vm_interface_daily_history', 'transmitted_dropped_total_packets', 'DECIMAL(18,4)');