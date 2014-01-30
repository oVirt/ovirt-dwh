--delete ad_domain column from vm_configuration table
SELECT fn_db_drop_column('vm_configuration', 'ad_domain');

