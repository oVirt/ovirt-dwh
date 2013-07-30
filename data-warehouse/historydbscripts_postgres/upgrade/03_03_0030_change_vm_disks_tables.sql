--drop old indexes on image_id
DROP INDEX vm_disk_configuration_vm_disk_id_idx;
DROP INDEX vm_disk_samples_history_vm_disk_id_idx;
DROP INDEX vm_disk_hourly_history_vm_disk_id_idx;
DROP INDEX vm_disk_daily_history_vm_disk_id_idx;

--change image_id to nullable and vm_disk_id to not nullable
ALTER TABLE vm_disk_configuration ALTER COLUMN image_id DROP NOT NULL;
ALTER TABLE vm_disk_samples_history ALTER COLUMN image_id DROP NOT NULL;
ALTER TABLE vm_disk_hourly_history ALTER COLUMN image_id DROP NOT NULL;
ALTER TABLE vm_disk_daily_history ALTER COLUMN image_id DROP NOT NULL;

--set empty GUID to pervent missing values
UPDATE vm_disk_configuration
SET vm_disk_id = cast('00000000-0000-0000-0000-000000000000' as UUID)
WHERE vm_disk_id IS NULL;

UPDATE vm_disk_samples_history
SET vm_disk_id = cast('00000000-0000-0000-0000-000000000000' as UUID)
WHERE vm_disk_id IS NULL;

UPDATE vm_disk_hourly_history
SET vm_disk_id = cast('00000000-0000-0000-0000-000000000000' as UUID)
WHERE vm_disk_id IS NULL;

UPDATE vm_disk_daily_history
SET vm_disk_id = cast('00000000-0000-0000-0000-000000000000' as UUID)
WHERE vm_disk_id IS NULL;

ALTER TABLE vm_disk_configuration ALTER COLUMN vm_disk_id SET NOT NULL;
ALTER TABLE vm_disk_samples_history ALTER COLUMN vm_disk_id SET NOT NULL;
ALTER TABLE vm_disk_hourly_history ALTER COLUMN vm_disk_id SET NOT NULL;
ALTER TABLE vm_disk_daily_history ALTER COLUMN vm_disk_id SET NOT NULL;

--now recreate indexes
CREATE INDEX vm_disk_configuration_vm_disk_id_idx ON vm_disk_configuration(vm_disk_id);
CREATE INDEX vm_disk_samples_history_vm_disk_id_idx ON vm_disk_samples_history(vm_disk_id);
CREATE INDEX vm_disk_hourly_history_vm_disk_id_idx ON vm_disk_hourly_history(vm_disk_id);
CREATE INDEX vm_disk_daily_history_vm_disk_id_idx ON vm_disk_daily_history(vm_disk_id);

--change daily time column type to date
ALTER TABLE vm_disks_usage_daily_history ALTER COLUMN history_datetime TYPE DATE;

--change disk description to 500 chars
ALTER TABLE vm_disk_configuration ALTER COLUMN vm_disk_description TYPE VARCHAR(500);
