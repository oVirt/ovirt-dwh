INSERT INTO history_configuration(var_name,var_value) SELECT 'MinimalETLVersion','3.3.4' WHERE not exists (SELECT var_name FROM history_configuration WHERE var_name = 'MinimalETLVersion');
UPDATE history_configuration SET var_value = '3.3.4' WHERE var_name = 'MinimalETLVersion';
