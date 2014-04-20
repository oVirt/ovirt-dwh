INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'lastDayAggr',date_trunc('day',CURRENT_TIMESTAMP) - interval '1 day'
WHERE not exists (SELECT var_name
                  FROM history_configuration
                  WHERE var_name = 'lastDayAggr');

INSERT INTO history_configuration(var_name,var_datetime)
SELECT 'lastHourAggr',date_trunc('hour',CURRENT_TIMESTAMP) - interval '1 hour'
WHERE not exists (SELECT var_name
                  FROM history_configuration
                  WHERE var_name = 'lastHourAggr');

INSERT INTO history_configuration(var_name,var_value,var_datetime)
SELECT 'firstSync','true',to_timestamp('01/01/2000', 'DD/MM/YYYY')
WHERE not exists (SELECT var_name
                  FROM history_configuration
                  WHERE var_name = 'firstSync');
