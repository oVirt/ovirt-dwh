--Changing lastHourAggr initial value to allow user to run reports after etl first start

UPDATE history_configuration
SET var_datetime = date_trunc('month',CURRENT_TIMESTAMP)
WHERE var_name = 'lastHourAggr';
