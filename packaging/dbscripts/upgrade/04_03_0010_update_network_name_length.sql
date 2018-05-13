-- Update host_interface_configuration table network_name filed length to 256

SELECT fn_db_change_column_type('host_interface_configuration', 'network_name', 'VARCHAR(50)', 'VARCHAR(256)');

-- Update vm_interface_configuration table network_name filed length to 256

SELECT fn_db_change_column_type('vm_interface_configuration', 'network_name', 'VARCHAR(50)', 'VARCHAR(256)');
