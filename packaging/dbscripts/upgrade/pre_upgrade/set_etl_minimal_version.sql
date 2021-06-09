INSERT INTO history_configuration(var_name,var_value) SELECT 'MinimalETLVersion','4.4.7' WHERE not exists (SELECT var_name FROM history_configuration WHERE var_name = 'MinimalETLVersion');
UPDATE history_configuration SET var_value = '4.4.7' WHERE var_name = 'MinimalETLVersion';
