select fn_db_drop_column('vm_disk_configuration', 'guest_disk_size_mb');
select fn_db_drop_column('vm_disk_samples_history', 'guest_used_disk_size_mb');
select fn_db_drop_column('vm_disk_hourly_history', 'guest_used_disk_size_mb');
select fn_db_drop_column('vm_disk_daily_history', 'guest_used_disk_size_mb');

CREATE OR REPLACE FUNCTION execute(TEXT) RETURNS VOID AS $$
BEGIN
  EXECUTE $1;
END; $$ LANGUAGE plpgsql;

SELECT execute($$ CREATE SEQUENCE vm_disks_usage_history_seq1 INCREMENT BY 1 START WITH 1;
		  CREATE TABLE vm_disks_usage_samples_history
			(
			   history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq1') PRIMARY KEY NOT NULL,
			   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
			   vm_id UUID NOT NULL,
			   disks_usage TEXT
			) WITH OIDS;
		  CREATE INDEX IDX_disks_usage_history_datetime_samples ON vm_disks_usage_samples_history (history_datetime);
		  CREATE INDEX IDX_disks_usage_vm_id_samples ON vm_disks_usage_samples_history (vm_id); $$) WHERE NOT EXISTS(SELECT 1 from pg_class t WHERE t.relname = 'vm_disks_usage_samples_history');

SELECT execute($$ CREATE SEQUENCE vm_disks_usage_history_seq2 INCREMENT BY 1 START WITH 1;
		  CREATE TABLE vm_disks_usage_hourly_history
			(
			   history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq2') PRIMARY KEY NOT NULL,
			   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
			   vm_id UUID NOT NULL,
			   disks_usage TEXT
			) WITH OIDS;
		  CREATE INDEX IDX_disks_usage_history_datetime_hourly ON vm_disks_usage_hourly_history (history_datetime);
		  CREATE INDEX IDX_disks_usage_vm_id_hourly ON vm_disks_usage_hourly_history (vm_id); $$) WHERE NOT EXISTS(SELECT 1 from pg_class t WHERE t.relname = 'vm_disks_usage_hourly_history');

SELECT execute($$ CREATE SEQUENCE vm_disks_usage_history_seq3 INCREMENT BY 1 START WITH 1;
		  CREATE TABLE vm_disks_usage_daily_history
			(
			   history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq3') PRIMARY KEY NOT NULL,
			   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
			   vm_id UUID NOT NULL,
			   disks_usage TEXT
			) WITH OIDS;
		  CREATE INDEX IDX_disks_usage_history_datetime_daily ON vm_disks_usage_daily_history (history_datetime);
		  CREATE INDEX IDX_disks_usage_vm_id_daily ON vm_disks_usage_daily_history (vm_id); $$) WHERE NOT EXISTS(SELECT 1 from pg_class t WHERE t.relname = 'vm_disks_usage_daily_history');

DROP FUNCTION execute(TEXT);
