INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'dcLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'dcLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hostLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hostLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hinterfaceLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hinterfaceLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vminterfaceLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vminterfaceLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'storageLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'storageLastDayAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmDiskLastDayAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmDiskLastDayAggr');

INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'dcLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'dcLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hostLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hostLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'hinterfaceLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'hinterfaceLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vminterfaceLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vminterfaceLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'storageLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'storageLastHourAggr');
INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'vmDiskLastHourAggr',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
				  FROM history_configuration 
				  WHERE var_name = 'vmDiskLastHourAggr');
INSERT INTO history_configuration(var_name,var_value,var_datetime)
SELECT 'firstSync','true',cast('01/01/2000 12:00:00 PM' as TIMESTAMP)
WHERE not exists (SELECT var_name
		  FROM history_configuration 
		  WHERE var_name = 'firstSync');
