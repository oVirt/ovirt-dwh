INSERT INTO history_configuration(var_name,var_value) SELECT 'default_language','en_US' WHERE not exists (SELECT var_name FROM history_configuration WHERE var_name = 'default_language');
UPDATE history_configuration SET var_value = 'en_US' WHERE var_name = 'default_language' and var_value = 'us-en';
