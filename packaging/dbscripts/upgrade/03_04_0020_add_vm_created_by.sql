select fn_db_add_column('vm_configuration', 'created_by_user_id', 'uuid');
select fn_db_add_column('vm_configuration', 'created_by_user_name', 'varchar(255)');
