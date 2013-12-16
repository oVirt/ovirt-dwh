-- Changed vm_ip type to text to allow match engine and allow more then 18 ip per vm
ALTER TABLE statistics_vms_users_usage_daily ALTER COLUMN vm_ip TYPE text;
ALTER TABLE statistics_vms_users_usage_hourly ALTER COLUMN vm_ip TYPE text;
