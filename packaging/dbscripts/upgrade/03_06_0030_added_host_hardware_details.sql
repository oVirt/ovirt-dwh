select fn_db_add_column('host_configuration', 'threads_per_core', 'smallint');
select fn_db_add_column('host_configuration', 'hardware_manufacturer', 'character varying(255)');
select fn_db_add_column('host_configuration', 'hardware_product_name', 'character varying(255)');
select fn_db_add_column('host_configuration', 'hardware_version', 'character varying(255)');
select fn_db_add_column('host_configuration', 'hardware_serial_number', 'character varying(255)');

