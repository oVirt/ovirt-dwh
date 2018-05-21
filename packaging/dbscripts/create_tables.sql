CREATE TABLE history_configuration
(
   var_name VARCHAR(50) NOT NULL,
   var_value VARCHAR(255),
   var_datetime TIMESTAMP WITH TIME ZONE,
   CONSTRAINT PK_history_configuration PRIMARY KEY(var_name)
) WITH OIDS;

CREATE TABLE enum_translator
(
   enum_type VARCHAR(40) NOT NULL,
   enum_key SMALLINT NOT NULL,
   language_code VARCHAR(40) NOT NULL,
   value TEXT NOT NULL,
   CONSTRAINT PK_enums PRIMARY KEY(enum_type,enum_key,language_code)
) WITH OIDS;

CREATE SEQUENCE configuration_seq INCREMENT BY 1 START WITH 1;

CREATE TABLE datacenter_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   datacenter_id UUID NOT NULL,
   datacenter_name VARCHAR(40) NOT NULL,
   datacenter_description VARCHAR(4000) NOT NULL,
   storage_type SMALLINT NOT NULL,
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX datacenter_configuration_datacenter_id_idx ON datacenter_configuration(datacenter_id);

CREATE SEQUENCE datacenter_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE datacenter_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('datacenter_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   datacenter_id UUID NOT NULL,
   datacenter_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   datacenter_configuration_version INTEGER NOT NULL REFERENCES datacenter_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_datacenter_history_datetime_samples ON datacenter_samples_history (history_datetime);
CREATE INDEX IDX_datacenter_configuration_version_samples ON datacenter_samples_history (datacenter_configuration_version);
CREATE INDEX datacenter_samples_history_datacenter_id_idx ON datacenter_samples_history(datacenter_id);

CREATE SEQUENCE datacenter_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE datacenter_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('datacenter_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   datacenter_id UUID NOT NULL,
   datacenter_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   datacenter_configuration_version INTEGER NOT NULL REFERENCES datacenter_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_datacenter_history_datetime_hourly ON datacenter_hourly_history (history_datetime);
CREATE INDEX IDX_datacenter_configuration_version_hourly ON datacenter_hourly_history (datacenter_configuration_version);
CREATE INDEX datacenter_hourly_history_datacenter_id_idx ON datacenter_hourly_history(datacenter_id);

CREATE SEQUENCE datacenter_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE datacenter_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('datacenter_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   datacenter_id UUID NOT NULL,
   datacenter_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   datacenter_configuration_version INTEGER NOT NULL REFERENCES datacenter_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_datacenter_history_datetime_daily ON datacenter_daily_history (history_datetime);
CREATE INDEX IDX_datacenter_configuration_version_daily ON datacenter_daily_history (datacenter_configuration_version);
CREATE INDEX datacenter_daily_history_datacenter_id_idx ON datacenter_daily_history(datacenter_id);

CREATE TABLE storage_domain_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   storage_domain_id UUID NOT NULL,
   storage_domain_name VARCHAR(250) NOT NULL,
   storage_domain_type SMALLINT NOT NULL,
   storage_type SMALLINT NOT NULL,
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX storage_domain_configuration_storage_domain_id_idx ON storage_domain_configuration(storage_domain_id);

CREATE SEQUENCE datacenter_storage_domain_map_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE datacenter_storage_domain_map
(
   history_id INTEGER DEFAULT NEXTVAL('datacenter_storage_domain_map_seq') PRIMARY KEY NOT NULL,
   storage_domain_id UUID NOT NULL,
   datacenter_id UUID NOT NULL,
   attach_date TIMESTAMP WITH TIME ZONE NOT NULL,
   detach_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX datacenter_storage_domain_map_storage_domain_id_idx ON datacenter_storage_domain_map(storage_domain_id);
CREATE INDEX datacenter_storage_domain_map_datacenter_id_idx ON datacenter_storage_domain_map(datacenter_id);

CREATE SEQUENCE storage_domain_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE storage_domain_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('storage_domain_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   storage_domain_id UUID NOT NULL,
   available_disk_size_gb INTEGER,
   used_disk_size_gb INTEGER,
   storage_configuration_version INTEGER REFERENCES storage_domain_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_storage_history_datetime_samples ON storage_domain_samples_history (history_datetime);
CREATE INDEX IDX_storage_configuration_version_samples ON storage_domain_samples_history (storage_configuration_version);
CREATE INDEX storage_domain_samples_history_storage_domain_id_idx ON storage_domain_samples_history(storage_domain_id);

CREATE SEQUENCE storage_domain_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE storage_domain_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('storage_domain_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   storage_domain_id UUID NOT NULL,
   available_disk_size_gb INTEGER,
   used_disk_size_gb INTEGER,
   storage_configuration_version INTEGER REFERENCES storage_domain_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_storage_history_datetime_hourly ON storage_domain_hourly_history (history_datetime);
CREATE INDEX IDX_storage_configuration_version_hourly ON storage_domain_hourly_history (storage_configuration_version);
CREATE INDEX storage_domain_hourly_history_storage_domain_id_idx ON storage_domain_hourly_history(storage_domain_id);

CREATE SEQUENCE storage_domain_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE storage_domain_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('storage_domain_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   storage_domain_id UUID NOT NULL,
   available_disk_size_gb INTEGER,
   used_disk_size_gb INTEGER,
   storage_configuration_version INTEGER REFERENCES storage_domain_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_storage_domain_history_datetime_daily ON storage_domain_daily_history (history_datetime);
CREATE INDEX IDX_storage_configuration_version_daily ON storage_domain_daily_history (storage_configuration_version);
CREATE INDEX storage_domain_daily_history_storage_domain_id_idx ON storage_domain_daily_history(storage_domain_id);

CREATE TABLE cluster_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   cluster_id UUID NOT NULL,
   cluster_name VARCHAR(40) NOT NULL,
   cluster_description VARCHAR(4000),
   datacenter_id UUID,
   cpu_name VARCHAR(255),
   compatibility_version VARCHAR(40) NOT NULL DEFAULT '2.2',
   datacenter_configuration_version INTEGER REFERENCES datacenter_configuration (history_id),
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX cluster_configuration_cluster_id_idx ON cluster_configuration(cluster_id);
CREATE INDEX cluster_configuration_datacenter_id_idx ON cluster_configuration(datacenter_id);

CREATE TABLE host_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   host_id UUID NOT NULL,
   host_unique_id VARCHAR(128),
   host_name VARCHAR(255) NOT NULL,
   cluster_id UUID NOT NULL,
   host_type SMALLINT NOT NULL DEFAULT 0,
   fqdn_or_ip VARCHAR(255) NOT NULL,
   memory_size_mb INTEGER,
   swap_size_mb INTEGER,
   cpu_model VARCHAR(255),
   number_of_cores SMALLINT,
   host_os VARCHAR(255),
   kernel_version VARCHAR(255),
   kvm_version VARCHAR(255),
   vdsm_version VARCHAR(40),
   vdsm_port INTEGER NOT NULL,
   cluster_configuration_version INTEGER REFERENCES cluster_configuration (history_id),
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE,
   number_of_sockets SMALLINT,
   cpu_speed_mh DECIMAL(18,0)
) WITH OIDS;

CREATE INDEX host_configuration_host_id_idx ON host_configuration(host_id);
CREATE INDEX host_configuration_cluster_id_idx ON host_configuration(cluster_id);

CREATE SEQUENCE host_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   host_id UUID NOT NULL,
   host_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   memory_usage_percent SMALLINT  DEFAULT 0,
   cpu_usage_percent SMALLINT,
   ksm_cpu_percent SMALLINT  DEFAULT 0,
   active_vms SMALLINT  DEFAULT 0,
   total_vms SMALLINT  DEFAULT 0,
   total_vms_vcpus INTEGER  DEFAULT 0,
   cpu_load INTEGER  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   swap_used_mb INTEGER,
   host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_history_datetime_samples ON host_samples_history (history_datetime);
CREATE INDEX IDX_host_configuration_version_samples ON host_samples_history (host_configuration_version);
CREATE INDEX host_samples_history_host_id_idx ON host_samples_history(host_id);


CREATE SEQUENCE host_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   host_id UUID NOT NULL,
   host_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   cpu_usage_percent SMALLINT,
   max_cpu_usage SMALLINT,
   ksm_cpu_percent SMALLINT  DEFAULT 0,
   max_ksm_cpu_percent SMALLINT  DEFAULT 0,
   active_vms SMALLINT  DEFAULT 0,
   max_active_vms SMALLINT  DEFAULT 0,
   total_vms SMALLINT  DEFAULT 0,
   max_total_vms SMALLINT  DEFAULT 0,
   total_vms_vcpus INTEGER  DEFAULT 0,
   max_total_vms_vcpus INTEGER  DEFAULT 0,
   cpu_load INTEGER  DEFAULT 0,
   max_cpu_load INTEGER  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   swap_used_mb INTEGER,
   max_swap_used_mb INTEGER,
   host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_history_datetime_hourly ON host_hourly_history (history_datetime);
CREATE INDEX IDX_host_configuration_version_hourly ON host_hourly_history (host_configuration_version);
CREATE INDEX host_hourly_history_host_id_idx ON host_hourly_history(host_id);

CREATE SEQUENCE host_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   host_id UUID NOT NULL,
   host_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   cpu_usage_percent SMALLINT,
   max_cpu_usage SMALLINT,
   ksm_cpu_percent SMALLINT  DEFAULT 0,
   max_ksm_cpu_percent SMALLINT  DEFAULT 0,
   active_vms SMALLINT  DEFAULT 0,
   max_active_vms SMALLINT  DEFAULT 0,
   total_vms SMALLINT  DEFAULT 0,
   max_total_vms SMALLINT  DEFAULT 0,
   total_vms_vcpus INTEGER  DEFAULT 0,
   max_total_vms_vcpus INTEGER  DEFAULT 0,
   cpu_load INTEGER  DEFAULT 0,
   max_cpu_load INTEGER  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   swap_used_mb INTEGER,
   max_swap_used_mb INTEGER,
   host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_history_datetime_daily ON host_daily_history (history_datetime);
CREATE INDEX IDX_host_configuration_version_daily ON host_daily_history (host_configuration_version);
CREATE INDEX host_daily_history_host_id_idx ON host_daily_history(host_id);

CREATE TABLE  host_interface_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   host_interface_id UUID NOT NULL,
   host_interface_name VARCHAR(50) NOT NULL,
   host_id UUID NOT NULL,
   host_interface_type SMALLINT,
   host_interface_speed_bps INTEGER,
   mac_address VARCHAR(59),
   network_name VARCHAR(256),
   ip_address VARCHAR(20),
   gateway VARCHAR(20),
   bond BOOLEAN,
   bond_name VARCHAR(50),
   vlan_id INTEGER,
   host_configuration_version INTEGER REFERENCES host_configuration (history_id),
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX host_interface_configuration_host_interface_id_idx ON host_interface_configuration(host_interface_id);
CREATE INDEX host_interface_configuration_host_id_idx ON host_interface_configuration(host_id);

CREATE SEQUENCE host_interface_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_interface_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_interface_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   host_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   host_interface_configuration_version INTEGER REFERENCES host_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_interface_history_datetime_samples ON host_interface_samples_history (history_datetime);
CREATE INDEX IDX_host_interface_configuration_version_samples ON host_interface_samples_history (host_interface_configuration_version);
CREATE INDEX host_interface_samples_history_host_interface_id_idx ON host_interface_samples_history(host_interface_id);

CREATE SEQUENCE host_interface_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_interface_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_interface_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   host_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   max_receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   max_transmit_rate_percent DECIMAL(18,4),
   host_interface_configuration_version INTEGER REFERENCES host_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_interface_history_datetime_hourly ON host_interface_hourly_history (history_datetime);
CREATE INDEX IDX_host_interface_configuration_version_hourly ON host_interface_hourly_history (host_interface_configuration_version);
CREATE INDEX host_interface_hourly_history_host_interface_id_idx ON host_interface_hourly_history(host_interface_id);

CREATE SEQUENCE host_interface_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE host_interface_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('host_interface_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   host_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   max_receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   max_transmit_rate_percent DECIMAL(18,4),
   host_interface_configuration_version INTEGER REFERENCES host_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_host_interface_history_datetime_daily ON host_interface_daily_history (history_datetime);
CREATE INDEX IDX_host_interface_configuration_version_daily ON host_interface_daily_history (host_interface_configuration_version);
CREATE INDEX host_interface_daily_history_host_interface_id_idx ON host_interface_daily_history(host_interface_id);

CREATE TABLE vm_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   vm_id UUID NOT NULL,
   vm_name VARCHAR(255) NOT NULL,
   vm_description VARCHAR(4000),
   vm_type SMALLINT,
   cluster_id UUID NOT NULL,
   template_id UUID NOT NULL,
   template_name VARCHAR(255),
   cpu_per_socket SMALLINT,
   number_of_sockets SMALLINT,
   memory_size_mb INTEGER,
   operating_system SMALLINT NOT NULL DEFAULT 0,
   ad_domain VARCHAR(40),
   default_host UUID,
   high_availability BOOLEAN,
   initialized BOOLEAN,
   stateless BOOLEAN,
   fail_back BOOLEAN,
   auto_suspend BOOLEAN  DEFAULT false,
   usb_policy SMALLINT,
   time_zone VARCHAR(40),
   cluster_configuration_version INTEGER REFERENCES cluster_configuration (history_id),
   default_host_configuration_version INTEGER REFERENCES host_configuration (history_id),
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX vm_configuration_vm_id_idx ON vm_configuration(vm_id);
CREATE INDEX vm_configuration_cluster_id_idx ON vm_configuration(cluster_id);

CREATE SEQUENCE disk_vm_device_history_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_device_history
(
  history_id INTEGER DEFAULT NEXTVAL('disk_vm_device_history_seq') PRIMARY KEY NOT NULL,
  vm_id uuid NOT NULL,
  device_id uuid NOT NULL,
  type character varying(30) NOT NULL,
  address character varying(255) NOT NULL,
  is_managed boolean NOT NULL DEFAULT false,
  is_plugged boolean,
  is_readonly boolean NOT NULL DEFAULT false,
  vm_configuration_version INTEGER,
  device_configuration_version INTEGER,
  create_date TIMESTAMP WITH TIME ZONE NOT NULL,
  update_date TIMESTAMP WITH TIME ZONE,
  delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX IDX_vm_device_history_vm_id_type ON vm_device_history (vm_id, type);

CREATE SEQUENCE vm_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   vm_id UUID NOT NULL,
   vm_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   cpu_usage_percent SMALLINT  DEFAULT 0,
   memory_usage_percent SMALLINT  DEFAULT 0,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   vm_ip VARCHAR(255),
   current_user_name VARCHAR(255),
   currently_running_on_host UUID,
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   current_host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_history_datetime_samples ON vm_samples_history (history_datetime);
CREATE INDEX IDX_vm_configuration_version_samples ON vm_samples_history (vm_configuration_version);
CREATE INDEX IDX_vm_current_host_configuration_samples ON vm_samples_history (current_host_configuration_version);
CREATE INDEX vm_samples_history_vm_id_idx ON vm_samples_history(vm_id);

CREATE SEQUENCE vm_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   vm_id UUID NOT NULL,
   vm_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   cpu_usage_percent SMALLINT  DEFAULT 0,
   max_cpu_usage SMALLINT,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   vm_ip VARCHAR(255),
   current_user_name VARCHAR(255),
   currently_running_on_host UUID,
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   current_host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_history_datetime_hourly ON vm_hourly_history (history_datetime);
CREATE INDEX IDX_vm_configuration_version_hourly ON vm_hourly_history (vm_configuration_version);
CREATE INDEX IDX_vm_current_host_configuration_hourly ON vm_hourly_history (current_host_configuration_version);
CREATE INDEX vm_hourly_history_vm_id_idx ON vm_hourly_history(vm_id);

CREATE SEQUENCE vm_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   vm_id UUID NOT NULL,
   vm_status SMALLINT NOT NULL,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   cpu_usage_percent SMALLINT  DEFAULT 0,
   max_cpu_usage SMALLINT,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   vm_ip VARCHAR(255),
   current_user_name VARCHAR(255),
   currently_running_on_host UUID,
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   current_host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_history_datetime_daily ON vm_daily_history (history_datetime);
CREATE INDEX IDX_vm_configuration_version_daily ON vm_daily_history (vm_configuration_version);
CREATE INDEX IDX_vm_current_host_configuration_daily ON vm_daily_history (current_host_configuration_version);
CREATE INDEX vm_daily_history_vm_id_idx ON vm_daily_history(vm_id);

CREATE TABLE  vm_interface_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   vm_interface_id UUID NOT NULL,
   vm_interface_name VARCHAR(50) NOT NULL,
   vm_id UUID,
   vm_interface_type SMALLINT,
   vm_interface_speed_bps INTEGER,
   mac_address VARCHAR(20),
   network_name VARCHAR(256),
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX vm_interface_configuration_vm_interface_id_idx ON vm_interface_configuration(vm_interface_id);
CREATE INDEX vm_interface_configuration_vm_id_idx ON vm_interface_configuration(vm_id);

CREATE SEQUENCE vm_interface_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_interface_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_interface_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   vm_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   vm_interface_configuration_version INTEGER REFERENCES vm_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_interface_history_datetime_samples ON vm_interface_samples_history(history_datetime);
CREATE INDEX IDX_vm_interface_configuration_version_samples ON vm_interface_samples_history(vm_interface_configuration_version);
CREATE INDEX vm_interface_samples_history_vm_interface_id_idx ON vm_interface_samples_history(vm_interface_id);

CREATE SEQUENCE vm_interface_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_interface_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_interface_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   vm_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   max_receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   max_transmit_rate_percent DECIMAL(18,4),
   vm_interface_configuration_version INTEGER REFERENCES vm_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_interface_history_datetime_hourly ON vm_interface_hourly_history(history_datetime);
CREATE INDEX IDX_vm_interface_configuration_version_hourly ON vm_interface_hourly_history(vm_interface_configuration_version);
CREATE INDEX vm_interface_hourly_history_vm_interface_id_idx ON vm_interface_hourly_history(vm_interface_id);


CREATE SEQUENCE vm_interface_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_interface_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_interface_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   vm_interface_id UUID NOT NULL,
   receive_rate_percent DECIMAL(18,4),
   max_receive_rate_percent DECIMAL(18,4),
   transmit_rate_percent DECIMAL(18,4),
   max_transmit_rate_percent DECIMAL(18,4),
   vm_interface_configuration_version INTEGER REFERENCES vm_interface_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_interface_history_datetime_daily ON vm_interface_daily_history(history_datetime);
CREATE INDEX IDX_vm_interface_configuration_version_daily ON vm_interface_daily_history(vm_interface_configuration_version);
CREATE INDEX vm_interface_daily_history_vm_interface_id_idx ON vm_interface_daily_history(vm_interface_id);

CREATE TABLE vm_disk_configuration
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   image_id UUID NOT NULL,
   storage_domain_id UUID,
   vm_internal_drive_mapping SMALLINT,
   vm_disk_description VARCHAR(4000),
   vm_disk_size_mb INTEGER,
   vm_disk_type SMALLINT,
   vm_disk_format SMALLINT,
   vm_disk_interface SMALLINT,
   create_date TIMESTAMP WITH TIME ZONE,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE,
   vm_disk_id UUID,
   vm_disk_name VARCHAR(255),
   is_shared BOOLEAN
) WITH OIDS;

CREATE INDEX vm_disk_configuration_vm_disk_id_idx ON vm_disk_configuration(image_id);
CREATE INDEX vm_disk_configuration_storage_domain_id_idx ON vm_disk_configuration(storage_domain_id);

CREATE SEQUENCE vm_disk_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disk_samples_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_disk_history_seq1') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   image_id UUID NOT NULL,
   vm_disk_status SMALLINT,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   vm_disk_actual_size_mb INTEGER NOT NULL,
   read_rate_bytes_per_second INTEGER,
   read_latency_seconds DECIMAL(18,9),
   write_rate_bytes_per_second  INTEGER,
   write_latency_seconds DECIMAL(18,9),
   flush_latency_seconds DECIMAL(18,9),
   vm_disk_configuration_version INTEGER REFERENCES vm_disk_configuration (history_id),
   vm_disk_id UUID
 ) WITH OIDS;

CREATE INDEX IDX_vm_disk_history_datetime_samples ON vm_disk_samples_history (history_datetime);
CREATE INDEX IDX_vm_disk_configuration_version_samples ON vm_disk_samples_history (vm_disk_configuration_version);
CREATE INDEX vm_disk_samples_history_vm_disk_id_idx ON vm_disk_samples_history(image_id);

CREATE SEQUENCE vm_disk_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disk_hourly_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_disk_history_seq2') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   image_id UUID NOT NULL,
   vm_disk_status SMALLINT,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   vm_disk_actual_size_mb INTEGER NOT NULL,
   read_rate_bytes_per_second INTEGER,
   max_read_rate_bytes_per_second INTEGER,
   read_latency_seconds DECIMAL(18,9),
   max_read_latency_seconds DECIMAL(18,9),
   write_rate_bytes_per_second  INTEGER,
   max_write_rate_bytes_per_second  INTEGER,
   write_latency_seconds DECIMAL(18,9),
   max_write_latency_seconds DECIMAL(18,9),
   flush_latency_seconds DECIMAL(18,9),
   max_flush_latency_seconds DECIMAL(18,9),
   vm_disk_configuration_version INTEGER REFERENCES vm_disk_configuration (history_id),
   vm_disk_id UUID
) WITH OIDS;

CREATE INDEX IDX_vm_disk_history_datetime_hourly ON vm_disk_hourly_history (history_datetime);
CREATE INDEX IDX_vm_disk_configuration_version_hourly ON vm_disk_hourly_history (vm_disk_configuration_version);
CREATE INDEX vm_disk_hourly_history_vm_disk_id_idx ON vm_disk_hourly_history(image_id);

CREATE SEQUENCE vm_disk_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disk_daily_history
(
   history_id INTEGER DEFAULT NEXTVAL('vm_disk_history_seq3') primary key NOT NULL,
   history_datetime DATE NOT NULL,
   image_id UUID NOT NULL,
   vm_disk_status SMALLINT,
   minutes_in_status DECIMAL(7,2) NOT NULL DEFAULT 1,
   vm_disk_actual_size_mb INTEGER NOT NULL,
   read_rate_bytes_per_second INTEGER,
   max_read_rate_bytes_per_second INTEGER,
   read_latency_seconds DECIMAL(18,9),
   max_read_latency_seconds DECIMAL(18,9),
   write_rate_bytes_per_second  INTEGER,
   max_write_rate_bytes_per_second  INTEGER,
   write_latency_seconds DECIMAL(18,9),
   max_write_latency_seconds DECIMAL(18,9),
   flush_latency_seconds DECIMAL(18,9),
   max_flush_latency_seconds DECIMAL(18,9),
   vm_disk_configuration_version INTEGER REFERENCES vm_disk_configuration (history_id),
   vm_disk_id UUID
) WITH OIDS;

CREATE INDEX IDX_vm_disk_history_datetime_daily ON vm_disk_daily_history (history_datetime);
CREATE INDEX IDX_vm_disk_configuration_version_daily ON vm_disk_daily_history (vm_disk_configuration_version);
CREATE INDEX vm_disk_daily_history_vm_disk_id_idx ON vm_disk_daily_history(image_id);

CREATE SEQUENCE vm_disks_usage_history_seq1 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disks_usage_samples_history
(
    history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq1') PRIMARY KEY NOT NULL,
    history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    vm_id UUID NOT NULL,
    disks_usage TEXT
) WITH OIDS;

CREATE INDEX IDX_disks_usage_history_datetime_samples ON vm_disks_usage_samples_history (history_datetime);
CREATE INDEX IDX_disks_usage_vm_id_samples ON vm_disks_usage_samples_history (vm_id);

CREATE SEQUENCE vm_disks_usage_history_seq2 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disks_usage_hourly_history
(
    history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq2') PRIMARY KEY NOT NULL,
    history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    vm_id UUID NOT NULL,
    disks_usage TEXT
) WITH OIDS;

CREATE INDEX IDX_disks_usage_history_datetime_hourly ON vm_disks_usage_hourly_history (history_datetime);
CREATE INDEX IDX_disks_usage_vm_id_hourly ON vm_disks_usage_hourly_history (vm_id);

CREATE SEQUENCE vm_disks_usage_history_seq3 INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_disks_usage_daily_history
(
    history_id INTEGER DEFAULT NEXTVAL('vm_disks_usage_history_seq3') PRIMARY KEY NOT NULL,
    history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    vm_id UUID NOT NULL,
    disks_usage TEXT
) WITH OIDS;

CREATE INDEX IDX_disks_usage_history_datetime_daily ON vm_disks_usage_daily_history (history_datetime);
CREATE INDEX IDX_disks_usage_vm_id_daily ON vm_disks_usage_daily_history (vm_id);

CREATE SEQUENCE disk_vm_map_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE disks_vm_map
(
   history_id INTEGER DEFAULT NEXTVAL('disk_vm_map_seq') PRIMARY KEY NOT NULL,
   vm_disk_id UUID NOT NULL,
   vm_id UUID NOT NULL,
   attach_date TIMESTAMP WITH TIME ZONE NOT NULL,
   detach_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX disks_vm_map_vm_disk_id_idx ON disks_vm_map(vm_disk_id);
CREATE INDEX disks_vm_map_vm_id_idx ON disks_vm_map(vm_id);

CREATE TABLE tag_details
(
   history_id INTEGER DEFAULT NEXTVAL('configuration_seq') PRIMARY KEY NOT NULL,
   tag_id UUID NOT NULL,
   tag_name VARCHAR(50) NOT NULL,
   tag_description VARCHAR(4000),
   tag_path VARCHAR(4000) NOT NULL,
   tag_level SMALLINT NOT NULL,
   create_date TIMESTAMP WITH TIME ZONE NOT NULL,
   update_date TIMESTAMP WITH TIME ZONE,
   delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX tag_details_tag_id_idx ON tag_details(tag_id);
CREATE INDEX tag_details_tag_path_idx ON tag_details(tag_path);
CREATE INDEX tag_details_tag_level_idx ON tag_details(tag_level);

CREATE SEQUENCE tag_relations_history_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE tag_relations_history
(
   history_id INTEGER NOT NULL DEFAULT NEXTVAL('tag_relations_history_seq') PRIMARY KEY NOT NULL,
   entity_id UUID NOT NULL,
   entity_type SMALLINT NOT NULL,
   parent_id UUID,
   attach_date TIMESTAMP WITH TIME ZONE NOT NULL,
   detach_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX IX_tag_relations_history ON tag_relations_history(entity_id,attach_date);
CREATE INDEX IX_tag_relations_history_1 ON tag_relations_history(entity_type);
CREATE INDEX tag_relations_history_parent_id_idx ON tag_relations_history(parent_id);

CREATE TABLE calendar
(
   the_datetime TIMESTAMP without time zone PRIMARY KEY NOT NULL,
   the_date date NOT NULL,
   the_year smallint NOT NULL,
   the_month smallint NOT NULL,
   month_name character varying(9) NOT NULL,
   the_day smallint NOT NULL,
   day_name character varying(9) NOT NULL,
   the_hour time without time zone NOT NULL
) WITH OIDS;

CREATE INDEX calendar_table_index ON calendar (the_date);
ALTER TABLE calendar CLUSTER ON calendar_table_index;

CREATE SEQUENCE schema_version_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE schema_version
(
    id INTEGER DEFAULT NEXTVAL('schema_version_seq') NOT NULL,
    "version" varchar(10) NOT NULL,
    script varchar(255) NOT NULL,
    checksum varchar(128),
    installed_by varchar(30) NOT NULL,
    started_at timestamp  DEFAULT now(),
    ended_at timestamp ,
    state character varying(15) NOT NULL,
    "current" boolean NOT NULL,
    "comment" text NULL default '',
    CONSTRAINT schema_version_primary_key PRIMARY KEY (id)
);
