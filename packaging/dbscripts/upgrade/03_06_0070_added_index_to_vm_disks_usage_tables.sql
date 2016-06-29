-- Add indexes to vm disks usage tables
CREATE INDEX idx_vm_disks_usage_samples_history_datetime_vm_id_samples
  ON vm_disks_usage_samples_history
  (history_datetime, vm_id);

CREATE INDEX idx_vm_disks_usage_hourly_history_datetime_vm_id_hourly
  ON vm_disks_usage_hourly_history
  (history_datetime, vm_id);

CREATE INDEX idx_vm_disks_usage_daily_history_datetime_vm_id_daily
  ON vm_disks_usage_daily_history
  (history_datetime, vm_id);
