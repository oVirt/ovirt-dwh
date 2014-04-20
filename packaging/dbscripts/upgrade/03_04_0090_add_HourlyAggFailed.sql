-- Add a flag to history_configuration when hourly aggregation failes
INSERT INTO history_configuration ( var_name, var_value)
SELECT 'HourlyAggFailed', 'false'
WHERE not exists (SELECT var_name
                  FROM history_configuration
                  WHERE var_name = 'HourlyAggFailed');
