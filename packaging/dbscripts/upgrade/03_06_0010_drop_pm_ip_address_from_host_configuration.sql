--delete pm_ip_address column from host_configuration table
SELECT fn_db_drop_column('host_configuration', 'pm_ip_address');

