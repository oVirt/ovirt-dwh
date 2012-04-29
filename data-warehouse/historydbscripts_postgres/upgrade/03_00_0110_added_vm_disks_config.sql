ALTER TABLE vm_disk_configuration RENAME COLUMN vm_disk_id TO image_id;
select fn_db_add_column('vm_disk_configuration', 'vm_disk_id', 'uuid');
select fn_db_add_column('vm_disk_configuration', 'vm_disk_name', 'varchar(255)');
select fn_db_add_column('vm_disk_configuration', 'vm_disk_description', 'varchar(500)');
select fn_db_add_column('vm_disk_configuration', 'is_shared', 'boolean');


ALTER TABLE vm_disk_samples_history RENAME COLUMN vm_disk_id TO image_id;
select fn_db_add_column('vm_disk_samples_history', 'vm_disk_id', 'uuid');

ALTER TABLE vm_disk_hourly_history RENAME COLUMN vm_disk_id TO image_id;
select fn_db_add_column('vm_disk_hourly_history', 'vm_disk_id', 'uuid');

ALTER TABLE vm_disk_daily_history RENAME COLUMN vm_disk_id TO image_id;
select fn_db_add_column('vm_disk_daily_history', 'vm_disk_id', 'uuid');
