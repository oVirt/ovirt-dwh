-- Changed vm_ip type to text to allow match engine and allow more then 18 ip per vm
ALTER TABLE vm_samples_history ALTER COLUMN vm_ip TYPE text;
ALTER TABLE vm_hourly_history ALTER COLUMN vm_ip TYPE text;
ALTER TABLE vm_daily_history ALTER COLUMN vm_ip TYPE text;
