INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'dcLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'dcLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hostLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hostLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hinterfaceLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hinterfaceLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vminterfaceLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vminterfaceLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'storageLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'storageLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmDiskLastDayAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmDiskLastDayAggr');

INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'dcLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'dcLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hostLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hostLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hinterfaceLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hinterfaceLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vminterfaceLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vminterfaceLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'storageLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'storageLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmDiskLastHourAggr',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmDiskLastHourAggr');
INSERT INTO history_configuration(var_name,var_value,var_datetime)
SELECT 'firstSync','true',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
		  FROM history_configuration 
		  WHERE var_name = 'firstSync');
