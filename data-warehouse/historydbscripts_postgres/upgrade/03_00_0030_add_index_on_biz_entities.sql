CREATE OR REPLACE FUNCTION execute(TEXT) RETURNS VOID AS $$
BEGIN
  EXECUTE $1;
END; $$ LANGUAGE plpgsql;

SELECT execute($$ CREATE INDEX datacenter_configuration_datacenter_id_idx ON datacenter_configuration(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_configuration' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX datacenter_samples_history_datacenter_id_idx ON datacenter_samples_history(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_samples_history' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX datacenter_hourly_history_datacenter_id_idx ON datacenter_hourly_history(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_hourly_history' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX datacenter_daily_history_datacenter_id_idx ON datacenter_daily_history(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_daily_history' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX datacenter_storage_domain_map_storage_domain_id_idx ON datacenter_storage_domain_map(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_storage_domain_map' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX datacenter_storage_domain_map_datacenter_id_idx ON datacenter_storage_domain_map(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'datacenter_storage_domain_map' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX storage_domain_configuration_storage_domain_id_idx ON storage_domain_configuration(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'storage_domain_configuration' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX storage_domain_samples_history_storage_domain_id_idx ON storage_domain_samples_history(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'storage_domain_samples_history' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX storage_domain_hourly_history_storage_domain_id_idx ON storage_domain_hourly_history(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'storage_domain_hourly_history' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX storage_domain_daily_history_storage_domain_id_idx ON storage_domain_daily_history(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'storage_domain_daily_history' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX cluster_configuration_cluster_id_idx ON cluster_configuration(cluster_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'cluster_configuration' AND a.attname = 'cluster_id');

SELECT execute($$ CREATE INDEX cluster_configuration_datacenter_id_idx ON cluster_configuration(datacenter_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'cluster_configuration' AND a.attname = 'datacenter_id');

SELECT execute($$ CREATE INDEX host_configuration_host_id_idx ON host_configuration(host_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_configuration' AND a.attname = 'host_id');

SELECT execute($$ CREATE INDEX host_configuration_cluster_id_idx ON host_configuration(cluster_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_configuration' AND a.attname = 'cluster_id');

SELECT execute($$ CREATE INDEX host_samples_history_host_id_idx ON host_samples_history(host_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_samples_history' AND a.attname = 'host_id');

SELECT execute($$ CREATE INDEX host_hourly_history_host_id_idx ON host_hourly_history(host_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_hourly_history' AND a.attname = 'host_id');

SELECT execute($$ CREATE INDEX host_daily_history_host_id_idx ON host_daily_history(host_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_daily_history' AND a.attname = 'host_id');

SELECT execute($$ CREATE INDEX host_interface_configuration_host_interface_id_idx ON host_interface_configuration(host_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_interface_configuration' AND a.attname = 'host_interface_id');

SELECT execute($$ CREATE INDEX host_interface_configuration_host_id_idx ON host_interface_configuration(host_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_interface_configuration' AND a.attname = 'host_id');

SELECT execute($$ CREATE INDEX host_interface_samples_history_host_interface_id_idx ON host_interface_samples_history(host_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_interface_samples_history' AND a.attname = 'host_interface_id');

SELECT execute($$ CREATE INDEX host_interface_hourly_history_host_interface_id_idx ON host_interface_hourly_history(host_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_interface_hourly_history' AND a.attname = 'host_interface_id');

SELECT execute($$ CREATE INDEX host_interface_daily_history_host_interface_id_idx ON host_interface_daily_history(host_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'host_interface_daily_history' AND a.attname = 'host_interface_id');

SELECT execute($$ CREATE INDEX vm_configuration_vm_id_idx ON vm_configuration(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_configuration' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX vm_configuration_cluster_id_idx ON vm_configuration(cluster_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_configuration' AND a.attname = 'cluster_id');

SELECT execute($$ CREATE INDEX vm_samples_history_vm_id_idx ON vm_samples_history(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_samples_history' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX vm_hourly_history_vm_id_idx ON vm_hourly_history(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_hourly_history' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX vm_daily_history_vm_id_idx ON vm_daily_history(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_daily_history' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX vm_interface_configuration_vm_interface_id_idx ON vm_interface_configuration(vm_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_interface_configuration' AND a.attname = 'vm_interface_id');

SELECT execute($$ CREATE INDEX vm_interface_configuration_vm_id_idx ON vm_interface_configuration(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_interface_configuration' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX vm_interface_samples_history_vm_interface_id_idx ON vm_interface_samples_history(vm_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_interface_samples_history' AND a.attname = 'vm_interface_id');

SELECT execute($$ CREATE INDEX vm_interface_hourly_history_vm_interface_id_idx ON vm_interface_hourly_history(vm_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_interface_hourly_history' AND a.attname = 'vm_interface_id');

SELECT execute($$ CREATE INDEX vm_interface_daily_history_vm_interface_id_idx ON vm_interface_daily_history(vm_interface_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_interface_daily_history' AND a.attname = 'vm_interface_id');

SELECT execute($$ CREATE INDEX vm_disk_configuration_vm_disk_id_idx ON vm_disk_configuration(vm_disk_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_disk_configuration' AND a.attname = 'vm_disk_id');

SELECT execute($$ CREATE INDEX vm_disk_configuration_storage_domain_id_idx ON vm_disk_configuration(storage_domain_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_disk_configuration' AND a.attname = 'storage_domain_id');

SELECT execute($$ CREATE INDEX vm_disk_samples_history_vm_disk_id_idx ON vm_disk_samples_history(vm_disk_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_disk_samples_history' AND a.attname = 'vm_disk_id');

SELECT execute($$ CREATE INDEX vm_disk_hourly_history_vm_disk_id_idx ON vm_disk_hourly_history(vm_disk_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_disk_hourly_history' AND a.attname = 'vm_disk_id');

SELECT execute($$ CREATE INDEX vm_disk_daily_history_vm_disk_id_idx ON vm_disk_daily_history(vm_disk_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'vm_disk_daily_history' AND a.attname = 'vm_disk_id');

SELECT execute($$ CREATE INDEX disks_vm_map_vm_disk_id_idx ON disks_vm_map(vm_disk_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'disks_vm_map' AND a.attname = 'vm_disk_id');

SELECT execute($$ CREATE INDEX disks_vm_map_vm_id_idx ON disks_vm_map(vm_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'disks_vm_map' AND a.attname = 'vm_id');

SELECT execute($$ CREATE INDEX tag_details_tag_id_idx ON tag_details(tag_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'tag_details' AND a.attname = 'tag_id');

SELECT execute($$ CREATE INDEX tag_relations_history_entity_id_idx ON tag_relations_history(entity_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'tag_relations_history' AND a.attname = 'entity_id');

SELECT execute($$ CREATE INDEX tag_relations_history_parent_id_idx ON tag_relations_history(parent_id)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'tag_relations_history' AND a.attname = 'parent_id');

SELECT execute($$ CREATE INDEX tag_details_tag_path_idx ON tag_details(tag_path)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'tag_details' AND a.attname = 'tag_path');

SELECT execute($$ CREATE INDEX tag_details_tag_level_idx ON tag_details(tag_level)  $$) WHERE NOT EXISTS(SELECT 1 from pg_class t, pg_class i, pg_index ix, pg_attribute a WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = 'tag_details' AND a.attname = 'tag_level');

DROP FUNCTION execute(TEXT);

