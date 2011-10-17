UPDATE history_configuration
SET var_name = 'lastHourAggr'
WHERE var_name = 'vmDiskLastHourAggr';

UPDATE history_configuration
SET var_name = 'lastDayAggr'
WHERE var_name = 'vmDiskLastDayAggr';

DELETE FROM history_configuration
WHERE   var_name like '%Last%Aggr';
