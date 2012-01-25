-- Changed daily table aggregated time to date type to pervent problems with joins when changing time zone of the database.
ALTER TABLE datacenter_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE storage_domain_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE host_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE host_interface_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE vm_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE vm_interface_daily_history ALTER COLUMN history_datetime TYPE date;
ALTER TABLE vm_disk_daily_history ALTER COLUMN history_datetime TYPE date;
