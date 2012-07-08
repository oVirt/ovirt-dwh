--samples
ALTER TABLE vm_samples_history DROP COLUMN vm_last_up_time;
ALTER TABLE vm_samples_history DROP COLUMN vm_last_boot_time;
--hourly
ALTER TABLE vm_hourly_history DROP COLUMN vm_last_up_time;
ALTER TABLE vm_hourly_history DROP COLUMN vm_last_boot_time;
--daily
ALTER TABLE vm_daily_history DROP COLUMN vm_last_up_time;
ALTER TABLE vm_daily_history DROP COLUMN vm_last_boot_time;
