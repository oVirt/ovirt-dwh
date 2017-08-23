-- Update vm_configuration table te,plate_name filed length to 255

SELECT fn_db_change_column_type('vm_configuration', 'template_name', 'VARCHAR', 'VARCHAR(255)');
