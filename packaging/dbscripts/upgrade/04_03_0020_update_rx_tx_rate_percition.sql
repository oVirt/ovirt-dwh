-- Update vm_interface_samples_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('vm_interface_samples_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_samples_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');

-- Update vm_interface_hourly_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('vm_interface_hourly_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_hourly_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_hourly_history', 'max_receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_hourly_history', 'max_transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');

-- Update vm_interface_daily_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('vm_interface_daily_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_daily_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_daily_history', 'max_receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('vm_interface_daily_history', 'max_transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');

-- Update host_interface_samples_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('host_interface_samples_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_samples_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');

-- Update host_interface_hourly_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('host_interface_hourly_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_hourly_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_hourly_history', 'max_receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_hourly_history', 'max_transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');

-- Update host_interface_daily_history table rx and tx rates fields precision
SELECT fn_db_change_column_type('host_interface_daily_history', 'receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_daily_history', 'transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_daily_history', 'max_receive_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');
SELECT fn_db_change_column_type('host_interface_daily_history', 'max_transmit_rate_percent', 'SMALLINT', 'DECIMAL(18,4)');