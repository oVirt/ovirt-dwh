/**************************************
           VERSIONED VIEWS (4.0)
**************************************/

CREATE OR REPLACE VIEW v4_0_enum_translator
 AS
SELECT
    enum_translator.enum_type as enum_type,
    enum_translator.enum_key as enum_key,
    enum_translator.value as value
FROM enum_translator INNER JOIN
            history_configuration ON
                (enum_translator.language_code = history_configuration.var_value
                and history_configuration.var_name = 'default_language');

CREATE OR REPLACE VIEW v4_0_configuration_history_datacenters
 AS
SELECT
      history_id as history_id,
      datacenter_id as datacenter_id,
      datacenter_name as datacenter_name,
      datacenter_description as datacenter_description,
      is_local_storage as is_local_storage,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM datacenter_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_datacenters
 AS
SELECT
      history_id as history_id,
      datacenter_id as datacenter_id,
      datacenter_name as datacenter_name,
      datacenter_description as datacenter_description,
      is_local_storage as is_local_storage,
      create_date as create_date,
      update_date as update_date
FROM datacenter_configuration
WHERE history_id in (SELECT max(a.history_id) FROM datacenter_configuration as a GROUP BY a.datacenter_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_map_history_datacenters_storage_domains
 AS
SELECT
    history_id as history_id,
    storage_domain_id as storage_domain_id,
    datacenter_id as datacenter_id,
    attach_date as attach_date,
    detach_date as detach_date
FROM         datacenter_storage_domain_map;

CREATE OR REPLACE VIEW v4_0_latest_map_datacenters_storage_domains
 AS
SELECT
    history_id as history_id,
    storage_domain_id as storage_domain_id,
    datacenter_id as datacenter_id,
    attach_date as attach_date
FROM         datacenter_storage_domain_map
WHERE history_id in (SELECT max(a.history_id) FROM datacenter_storage_domain_map as a GROUP BY a.storage_domain_id, a.datacenter_id)
      and detach_date IS NULL;

CREATE OR REPLACE VIEW v4_0_configuration_history_storage_domains
 AS
SELECT
      history_id as history_id,
      storage_domain_id as storage_domain_id,
      storage_domain_name as storage_domain_name,
      storage_domain_type as storage_domain_type,
      storage_type as storage_type,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM storage_domain_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_storage_domains
 AS
SELECT
      history_id as history_id,
      storage_domain_id as storage_domain_id,
      storage_domain_name as storage_domain_name,
      storage_domain_type as storage_domain_type,
      storage_type as storage_type,
      create_date as create_date,
      update_date as update_date
FROM storage_domain_configuration
WHERE history_id in (SELECT max(a.history_id) FROM storage_domain_configuration as a GROUP BY a.storage_domain_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_storage_domains_resources_usage_samples
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      storage_domain_id as storage_domain_id,
      storage_domain_status,
      seconds_in_status as seconds_in_status,
      cast(seconds_in_status as numeric(7,2)) / 60 as minutes_in_status,
      available_disk_size_gb as available_disk_size_gb,
      used_disk_size_gb as used_disk_size_gb,
      storage_configuration_version as storage_configuration_version
FROM storage_domain_samples_history;

CREATE OR REPLACE VIEW v4_0_statistics_storage_domains_resources_usage_hourly
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      storage_domain_id as storage_domain_id,
      storage_domain_status,
      cast(minutes_in_status * 60 as integer) as seconds_in_status,
      minutes_in_status,
      available_disk_size_gb as available_disk_size_gb,
      used_disk_size_gb as used_disk_size_gb,
      storage_configuration_version as storage_configuration_version
FROM storage_domain_hourly_history;

CREATE OR REPLACE VIEW v4_0_statistics_storage_domains_resources_usage_daily
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      storage_domain_id as storage_domain_id,
      storage_domain_status,
      cast(minutes_in_status * 60 as integer) as seconds_in_status,
      minutes_in_status,
      available_disk_size_gb as available_disk_size_gb,
      used_disk_size_gb as used_disk_size_gb,
      storage_configuration_version as storage_configuration_version
FROM storage_domain_daily_history;

CREATE OR REPLACE VIEW v4_0_configuration_history_clusters
 AS
SELECT
      history_id as history_id,
      cluster_id as cluster_id,
      cluster_name as cluster_name,
      cluster_description as cluster_description,
      datacenter_id as datacenter_id,
      cpu_name as cpu_name,
      compatibility_version as compatibility_version,
      datacenter_configuration_version as datacenter_configuration_version,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM cluster_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_clusters
 AS
SELECT
      history_id as history_id,
      cluster_id as cluster_id,
      cluster_name as cluster_name,
      cluster_description as cluster_description,
      datacenter_id as datacenter_id,
      cpu_name as cpu_name,
      compatibility_version as compatibility_version,
      datacenter_configuration_version as datacenter_configuration_version,
      create_date as create_date,
      update_date as update_date
FROM cluster_configuration
WHERE history_id in (SELECT max(a.history_id) FROM cluster_configuration as a GROUP BY a.cluster_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_configuration_history_hosts
 AS
SELECT
      history_id as history_id,
      host_id as host_id,
      host_unique_id as host_unique_id,
      host_name as host_name,
      cluster_id as cluster_id,
      host_type as host_type,
      fqdn_or_ip as fqdn_or_ip,
      memory_size_mb as memory_size_mb,
      swap_size_mb as swap_size_mb,
      cpu_model as cpu_model,
      number_of_cores as number_of_cores,
      number_of_sockets,
      cpu_speed_mh,
      host_os as host_os,
      kernel_version as kernel_version,
      kvm_version as kvm_version,
      CASE SUBSTR(vdsm_version,1,3)
        WHEN '4.4' THEN '2.1' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
        WHEN '4.5' THEN '2.2' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
        WHEN '4.9' THEN '2.3' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
      ELSE vdsm_version
      END as vdsm_version,
      vdsm_port as vdsm_port,
      threads_per_core as threads_per_core,
      hardware_manufacturer as hardware_manufacturer,
      hardware_product_name as hardware_product_name,
      hardware_version as hardware_version,
      hardware_serial_number as hardware_serial_number,
      cluster_configuration_version as cluster_configuration_version,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM host_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_hosts
 AS
SELECT
      history_id as history_id,
      host_id as host_id,
      host_unique_id as host_unique_id,
      host_name as host_name,
      cluster_id as cluster_id,
      host_type as host_type,
      fqdn_or_ip as fqdn_or_ip,
      memory_size_mb as memory_size_mb,
      swap_size_mb as swap_size_mb,
      cpu_model as cpu_model,
      number_of_cores as number_of_cores,
      number_of_sockets,
      cpu_speed_mh,
      host_os as host_os,
      kernel_version as kernel_version,
      kvm_version as kvm_version,
      CASE SUBSTR(vdsm_version,1,3)
        WHEN '4.4' THEN '2.1' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
        WHEN '4.5' THEN '2.2' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
        WHEN '4.9' THEN '2.3' || SUBSTR(vdsm_version,4,LENGTH(vdsm_version))
      ELSE vdsm_version
      END as vdsm_version,
      vdsm_port as vdsm_port,
      threads_per_core as threads_per_core,
      hardware_manufacturer as hardware_manufacturer,
      hardware_product_name as hardware_product_name,
      hardware_version as hardware_version,
      hardware_serial_number as hardware_serial_number,
      cluster_configuration_version as cluster_configuration_version,
      create_date as create_date,
      update_date as update_date
FROM host_configuration
WHERE history_id in (SELECT max(a.history_id) FROM host_configuration as a GROUP BY a.host_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_resources_usage_samples
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_id as host_id,
      host_status as host_status,
      seconds_in_status as seconds_in_status,
      cast(seconds_in_status as numeric(7,2)) / 60 as minutes_in_status,
      memory_usage_percent as memory_usage_percent,
      ksm_shared_memory_mb,
      cpu_usage_percent as cpu_usage_percent,
      ksm_cpu_percent as ksm_cpu_percent,
      active_vms as active_vms,
      total_vms as total_vms,
      total_vms_vcpus as total_vms_vcpus,
      cpu_load as cpu_load,
      system_cpu_usage_percent as system_cpu_usage_percent,
      user_cpu_usage_percent as user_cpu_usage_percent,
      swap_used_mb as swap_used_mb,
      host_configuration_version as host_configuration_version
FROM host_samples_history;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_resources_usage_hourly
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_id as host_id,
      host_status as host_status,
      cast(minutes_in_status * 60 as integer) as seconds_in_status,
      minutes_in_status as minutes_in_status,
      memory_usage_percent as memory_usage_percent,
      max_memory_usage as max_memory_usage,
      ksm_shared_memory_mb,
      max_ksm_shared_memory_mb,
      cpu_usage_percent as cpu_usage_percent,
      max_cpu_usage as max_cpu_usage,
      ksm_cpu_percent as ksm_cpu_percent,
      max_ksm_cpu_percent as max_ksm_cpu_percent,
      active_vms as active_vms,
      max_active_vms as max_active_vms,
      total_vms as total_vms,
      max_total_vms as max_total_vms,
      total_vms_vcpus as total_vms_vcpus,
      max_total_vms_vcpus as max_total_vms_vcpus,
      cpu_load as cpu_load,
      max_cpu_load as max_cpu_load,
      system_cpu_usage_percent as system_cpu_usage_percent,
      max_system_cpu_usage_percent as max_system_cpu_usage_percent,
      user_cpu_usage_percent as user_cpu_usage_percent,
      max_user_cpu_usage_percent as max_user_cpu_usage_percent,
      swap_used_mb as swap_used_mb,
      max_swap_used_mb as max_swap_used_mb,
      host_configuration_version as host_configuration_version
FROM host_hourly_history;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_resources_usage_daily
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_id as host_id,
      host_status as host_status,
      cast(minutes_in_status * 60 as integer) as seconds_in_status,
      minutes_in_status as minutes_in_status,
      memory_usage_percent as memory_usage_percent,
      max_memory_usage as max_memory_usage,
      ksm_shared_memory_mb,
      max_ksm_shared_memory_mb,
      cpu_usage_percent as cpu_usage_percent,
      max_cpu_usage as max_cpu_usage,
      ksm_cpu_percent as ksm_cpu_percent,
      max_ksm_cpu_percent as max_ksm_cpu_percent,
      active_vms as active_vms,
      max_active_vms as max_active_vms,
      total_vms as total_vms,
      max_total_vms as max_total_vms,
      total_vms_vcpus as total_vms_vcpus,
      max_total_vms_vcpus as max_total_vms_vcpus,
      cpu_load as cpu_load,
      max_cpu_load as max_cpu_load,
      system_cpu_usage_percent as system_cpu_usage_percent,
      max_system_cpu_usage_percent as max_system_cpu_usage_percent,
      user_cpu_usage_percent as user_cpu_usage_percent,
      max_user_cpu_usage_percent as max_user_cpu_usage_percent,
      swap_used_mb as swap_used_mb,
      max_swap_used_mb as max_swap_used_mb,
      host_configuration_version as host_configuration_version
FROM host_daily_history;

CREATE OR REPLACE VIEW v4_0_configuration_history_hosts_interfaces
 AS
SELECT
      history_id as history_id,
      host_interface_id as host_interface_id,
      host_interface_name as host_interface_name,
      host_id as host_id,
      host_interface_type as host_interface_type,
      host_interface_speed_bps as host_interface_speed_bps,
      mac_address as mac_address,
      logical_network_name,
      ip_address as ip_address,
      gateway as gateway,
      bond as bond,
      bond_name as bond_name,
      vlan_id as vlan_id,
      host_configuration_version as host_configuration_version,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM host_interface_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_hosts_interfaces
 AS
SELECT
      history_id as history_id,
      host_interface_id as host_interface_id,
      host_interface_name as host_interface_name,
      host_id as host_id,
      host_interface_type as host_interface_type,
      host_interface_speed_bps as host_interface_speed_bps,
      mac_address as mac_address,
      logical_network_name,
      ip_address as ip_address,
      gateway as gateway,
      bond as bond,
      bond_name as bond_name,
      vlan_id as vlan_id,
      host_configuration_version as host_configuration_version,
      create_date as create_date,
      update_date as update_date
FROM host_interface_configuration
WHERE history_id in (SELECT max(a.history_id) FROM host_interface_configuration as a GROUP BY a.host_interface_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_interfaces_resources_usage_samples
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_interface_id as host_interface_id,
      receive_rate_percent as receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      host_interface_configuration_version as host_interface_configuration_version
FROM host_interface_samples_history;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_interfaces_resources_usage_hourly
 AS
SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_interface_id as host_interface_id,
      receive_rate_percent as receive_rate_percent,
      max_receive_rate_percent as max_receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      max_transmit_rate_percent as max_transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      host_interface_configuration_version as host_interface_configuration_version
FROM host_interface_hourly_history;

CREATE OR REPLACE VIEW v4_0_statistics_hosts_interfaces_resources_usage_daily
 AS

SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      host_interface_id as host_interface_id,
      receive_rate_percent as receive_rate_percent,
      max_receive_rate_percent as max_receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      max_transmit_rate_percent as max_transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      host_interface_configuration_version as host_interface_configuration_version
FROM host_interface_daily_history;

CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_hosts_resources_usage_samples
 AS
SELECT
    conf.host_id as host_id,
    conf.host_unique_id as host_unique_id,
    conf.host_name as host_name,
    conf.cluster_id as cluster_id,
    conf.host_type as host_type,
    conf.fqdn_or_ip as fqdn_or_ip,
    conf.memory_size_mb as memory_size_mb,
    conf.swap_size_mb as swap_size_mb,
    conf.cpu_model as cpu_model,
    conf.number_of_cores as number_of_cores,
    conf.number_of_sockets as number_of_sockets,
    conf.cpu_speed_mh as cpu_speed_mh,
    conf.host_os as host_os,
    conf.kernel_version as kernel_version,
    conf.kvm_version as kvm_version,
    conf.vdsm_version as vdsm_version,
    conf.vdsm_port as vdsm_port,
    conf.threads_per_core as threads_per_core,
    conf.hardware_manufacturer as hardware_manufacturer,
    conf.hardware_product_name as hardware_product_name,
    conf.hardware_version as hardware_version,
    conf.hardware_serial_number as hardware_serial_number,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.create_date as host_create_date,
    conf.update_date as host_update_date,
    conf.delete_date as host_delete_date,
    stats.history_datetime as history_datetime,
    stats.host_status as host_status,
    stats.seconds_in_status as host_seconds_in_status,
    cast(stats.seconds_in_status as numeric(7,2)) / 60 as host_minutes_in_status,
    stats.memory_usage_percent as memory_usage_percent,
    stats.ksm_shared_memory_mb ksm_shared_memory_mb,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.ksm_cpu_percent as ksm_cpu_percent,
    stats.active_vms as active_vms,
    stats.total_vms as total_vms,
    stats.total_vms_vcpus as total_vms_vcpus,
    stats.cpu_load as cpu_load,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.swap_used_mb as swap_used_mb,
    nic_conf.host_interface_id as host_interface_id,
    nic_conf.host_interface_name as host_interface_name,
    nic_conf.host_interface_type as host_interface_type,
    nic_conf.host_interface_speed_bps as host_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name,
    nic_conf.ip_address as ip_address,
    nic_conf.gateway as gateway,
    nic_conf.bond as bond,
    nic_conf.bond_name as bond_name,
    nic_conf.vlan_id as vlan_id,
    nic_conf.create_date as host_interface_create_date,
    nic_conf.update_date as host_interface_update_date,
    nic_conf.delete_date as host_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte
FROM v4_0_configuration_history_hosts AS conf
    LEFT OUTER JOIN v4_0_statistics_hosts_resources_usage_samples AS stats
        ON (conf.history_id = stats.host_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_hosts_interfaces nic_conf
        ON (conf.history_id = nic_conf.host_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_hosts_interfaces_resources_usage_samples nic_stats
        ON (nic_conf.history_id = nic_stats.host_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime);


CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_hosts_resources_usage_hourly
 AS
SELECT
    conf.host_id as host_id,
    conf.host_unique_id as host_unique_id,
    conf.host_name as host_name,
    conf.cluster_id as cluster_id,
    conf.host_type as host_type,
    conf.fqdn_or_ip as fqdn_or_ip,
    conf.memory_size_mb as memory_size_mb,
    conf.swap_size_mb as swap_size_mb,
    conf.cpu_model as cpu_model,
    conf.number_of_cores as number_of_cores,
    conf.number_of_sockets as number_of_sockets,
    conf.cpu_speed_mh as cpu_speed_mh,
    conf.host_os as host_os,
    conf.kernel_version as kernel_version,
    conf.kvm_version as kvm_version,
    conf.vdsm_version as vdsm_version,
    conf.vdsm_port as vdsm_port,
    conf.threads_per_core as threads_per_core,
    conf.hardware_manufacturer as hardware_manufacturer,
    conf.hardware_product_name as hardware_product_name,
    conf.hardware_version as hardware_version,
    conf.hardware_serial_number as hardware_serial_number,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.create_date as host_create_date,
    conf.update_date as host_update_date,
    conf.delete_date as host_delete_date,
    stats.history_datetime as history_datetime,
    stats.host_status as host_status,
    cast(stats.minutes_in_status * 60 as integer) as host_seconds_in_status,
    stats.minutes_in_status as host_minutes_in_status,
    stats.memory_usage_percent as memory_usage_percent,
    stats.max_memory_usage as max_memory_usage,
    stats.ksm_shared_memory_mb ksm_shared_memory_mb,
    stats.max_ksm_shared_memory_mb as max_ksm_shared_memory_mb,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.max_cpu_usage as max_cpu_usage,
    stats.ksm_cpu_percent as ksm_cpu_percent,
    stats.max_ksm_cpu_percent as max_ksm_cpu_percent,
    stats.active_vms as active_vms,
    stats.max_active_vms as max_active_vms,
    stats.total_vms as total_vms,
    stats.max_total_vms as max_total_vms,
    stats.total_vms_vcpus as total_vms_vcpus,
    stats.max_total_vms_vcpus as max_total_vms_vcpus,
    stats.cpu_load as cpu_load,
    stats.max_cpu_load as max_cpu_load,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    stats.swap_used_mb as swap_used_mb,
    stats.max_swap_used_mb as max_swap_used_mb,
    nic_conf.host_interface_id as host_interface_id,
    nic_conf.host_interface_name as host_interface_name,
    nic_conf.host_interface_type as host_interface_type,
    nic_conf.host_interface_speed_bps as host_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name,
    nic_conf.ip_address as ip_address,
    nic_conf.gateway as gateway,
    nic_conf.bond as bond,
    nic_conf.bond_name as bond_name,
    nic_conf.vlan_id as vlan_id,
    nic_conf.create_date as host_interface_create_date,
    nic_conf.update_date as host_interface_update_date,
    nic_conf.delete_date as host_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.max_receive_rate_percent as max_receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.max_transmit_rate_percent as max_transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte
FROM v4_0_configuration_history_hosts AS conf
    LEFT OUTER JOIN v4_0_statistics_hosts_resources_usage_hourly AS stats
        ON (conf.history_id = stats.host_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_hosts_interfaces nic_conf
        ON (conf.history_id = nic_conf.host_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_hosts_interfaces_resources_usage_hourly nic_stats
        ON (nic_conf.history_id = nic_stats.host_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime);


CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_hosts_resources_usage_daily
 AS
SELECT
    conf.host_id as host_id,
    conf.host_unique_id as host_unique_id,
    conf.host_name as host_name,
    conf.cluster_id as cluster_id,
    conf.host_type as host_type,
    conf.fqdn_or_ip as fqdn_or_ip,
    conf.memory_size_mb as memory_size_mb,
    conf.swap_size_mb as swap_size_mb,
    conf.cpu_model as cpu_model,
    conf.number_of_cores as number_of_cores,
    conf.number_of_sockets as number_of_sockets,
    conf.cpu_speed_mh as cpu_speed_mh,
    conf.host_os as host_os,
    conf.kernel_version as kernel_version,
    conf.kvm_version as kvm_version,
    conf.vdsm_version as vdsm_version,
    conf.vdsm_port as vdsm_port,
    conf.threads_per_core as threads_per_core,
    conf.hardware_manufacturer as hardware_manufacturer,
    conf.hardware_product_name as hardware_product_name,
    conf.hardware_version as hardware_version,
    conf.hardware_serial_number as hardware_serial_number,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.create_date as host_create_date,
    conf.update_date as host_update_date,
    conf.delete_date as host_delete_date,
    stats.history_datetime as history_datetime,
    stats.host_status as host_status,
    cast(stats.minutes_in_status * 60 as integer) as host_seconds_in_status,
    stats.minutes_in_status as host_minutes_in_status,
    stats.memory_usage_percent as memory_usage_percent,
    stats.max_memory_usage as max_memory_usage,
    stats.ksm_shared_memory_mb ksm_shared_memory_mb,
    stats.max_ksm_shared_memory_mb as max_ksm_shared_memory_mb,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.max_cpu_usage as max_cpu_usage,
    stats.ksm_cpu_percent as ksm_cpu_percent,
    stats.max_ksm_cpu_percent as max_ksm_cpu_percent,
    stats.active_vms as active_vms,
    stats.max_active_vms as max_active_vms,
    stats.total_vms as total_vms,
    stats.max_total_vms as max_total_vms,
    stats.total_vms_vcpus as total_vms_vcpus,
    stats.max_total_vms_vcpus as max_total_vms_vcpus,
    stats.cpu_load as cpu_load,
    stats.max_cpu_load as max_cpu_load,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    stats.swap_used_mb as swap_used_mb,
    stats.max_swap_used_mb as max_swap_used_mb,
    nic_conf.host_interface_id as host_interface_id,
    nic_conf.host_interface_name as host_interface_name,
    nic_conf.host_interface_type as host_interface_type,
    nic_conf.host_interface_speed_bps as host_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name,
    nic_conf.ip_address as ip_address,
    nic_conf.gateway as gateway,
    nic_conf.bond as bond,
    nic_conf.bond_name as bond_name,
    nic_conf.vlan_id as vlan_id,
    nic_conf.create_date as host_interface_create_date,
    nic_conf.update_date as host_interface_update_date,
    nic_conf.delete_date as host_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.max_receive_rate_percent as max_receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.max_transmit_rate_percent as max_transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte
FROM v4_0_configuration_history_hosts AS conf
    LEFT OUTER JOIN v4_0_statistics_hosts_resources_usage_daily AS stats
        ON (conf.history_id = stats.host_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_hosts_interfaces nic_conf
        ON (conf.history_id = nic_conf.host_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_hosts_interfaces_resources_usage_daily nic_stats
        ON (nic_conf.history_id = nic_stats.host_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime);


CREATE OR REPLACE VIEW v4_0_configuration_history_vms
 AS
SELECT
      history_id as history_id,
      vm_id as vm_id,
      vm_name as vm_name,
      vm_description as vm_description,
      vm_type as vm_type,
      cluster_id as cluster_id,
      template_id as template_id,
      template_name as template_name,
      cpu_per_socket as cpu_per_socket,
      number_of_sockets as number_of_sockets,
      memory_size_mb as memory_size_mb,
      operating_system as operating_system,
      default_host as default_host,
      high_availability as high_availability,
      initialized as initialized,
      stateless as stateless,
      fail_back as fail_back,
      usb_policy as usb_policy,
      time_zone as time_zone,
      vm_pool_id,
      vm_pool_name,
      created_by_user_id,
      cluster_configuration_version as cluster_configuration_version,
      default_host_configuration_version as default_host_configuration_version,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM vm_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_vms
 AS
SELECT
      history_id as history_id,
      vm_id as vm_id,
      vm_name as vm_name,
      vm_description as vm_description,
      vm_type as vm_type,
      cluster_id as cluster_id,
      template_id as template_id,
      template_name as template_name,
      cpu_per_socket as cpu_per_socket,
      number_of_sockets as number_of_sockets,
      memory_size_mb as memory_size_mb,
      operating_system as operating_system,
      default_host as default_host,
      high_availability as high_availability,
      initialized as initialized,
      stateless as stateless,
      fail_back as fail_back,
      usb_policy as usb_policy,
      time_zone as time_zone,
      vm_pool_id,
      vm_pool_name,
      created_by_user_id,
      cluster_configuration_version as cluster_configuration_version,
      default_host_configuration_version as default_host_configuration_version,
      create_date as create_date,
      update_date as update_date
FROM vm_configuration
WHERE history_id in (SELECT max(a.history_id) FROM vm_configuration as a GROUP BY a.vm_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_vms_resources_usage_samples
 AS
SELECT
    a.history_id as history_id,
    a.history_datetime as history_datetime,
    a.vm_id as vm_id,
    a.vm_status as vm_status,
    a.seconds_in_status as seconds_in_status,
    cast(a.seconds_in_status as numeric(7,2)) / 60 as minutes_in_status,
    a.cpu_usage_percent as cpu_usage_percent,
    a.memory_usage_percent as memory_usage_percent,
    a.user_cpu_usage_percent as user_cpu_usage_percent,
    a.system_cpu_usage_percent as system_cpu_usage_percent,
    a.vm_ip as vm_ip,
    a.vm_client_ip,
    a.currently_running_on_host as currently_running_on_host,
    a.current_user_id as current_user_id,
    a.user_logged_in_to_guest,
    b.disks_usage as disks_usage,
    a.vm_configuration_version as vm_configuration_version,
    a.current_host_configuration_version as current_host_configuration_version,
    a.memory_buffered_kb as memory_buffered_kb,
    a.memory_cached_kb as memory_cached_kb
FROM     vm_samples_history as a
        LEFT OUTER JOIN vm_disks_usage_samples_history as b
            ON (a.history_datetime = b.history_datetime AND a.vm_id = b.vm_id);

CREATE OR REPLACE VIEW v4_0_statistics_vms_resources_usage_hourly
 AS
SELECT
    a.history_id as history_id,
    a.history_datetime as history_datetime,
    a.vm_id as vm_id,
    a.vm_status as vm_status,
    cast(a.minutes_in_status * 60 as integer) as seconds_in_status,
    a.minutes_in_status as minutes_in_status,
    a.cpu_usage_percent as cpu_usage_percent,
    a.max_cpu_usage as max_cpu_usage,
    a.memory_usage_percent as memory_usage_percent,
    a.max_memory_usage as max_memory_usage,
    a.user_cpu_usage_percent as user_cpu_usage_percent,
    a.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    a.system_cpu_usage_percent as system_cpu_usage_percent,
    a.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    a.vm_ip as vm_ip,
    a.currently_running_on_host as currently_running_on_host,
    a.current_user_id as current_user_id,
    b.disks_usage as disks_usage,
    a.vm_configuration_version as vm_configuration_version,
    a.current_host_configuration_version as current_host_configuration_version,
    a.memory_buffered_kb as memory_buffered_kb,
    a.memory_cached_kb as memory_cached_kb,
    a.max_memory_buffered_kb as max_memory_buffered_kb,
    a.max_memory_cached_kb as max_memory_cached_kb
FROM     vm_hourly_history as a
        LEFT OUTER JOIN vm_disks_usage_hourly_history as b
            ON (a.history_datetime = b.history_datetime AND a.vm_id = b.vm_id);

CREATE OR REPLACE VIEW v4_0_statistics_vms_resources_usage_daily
 AS
SELECT
    a.history_id as history_id,
    a.history_datetime as history_datetime,
    a.vm_id as vm_id,
    a.vm_status as vm_status,
    cast(a.minutes_in_status * 60 as integer) as seconds_in_status,
    a.minutes_in_status as minutes_in_status,
    a.cpu_usage_percent as cpu_usage_percent,
    a.max_cpu_usage as max_cpu_usage,
    a.memory_usage_percent as memory_usage_percent,
    a.max_memory_usage as max_memory_usage,
    a.user_cpu_usage_percent as user_cpu_usage_percent,
    a.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    a.system_cpu_usage_percent as system_cpu_usage_percent,
    a.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    a.vm_ip as vm_ip,
    a.currently_running_on_host as currently_running_on_host,
    a.current_user_id as current_user_id,
    b.disks_usage as disks_usage,
    a.vm_configuration_version as vm_configuration_version,
    a.current_host_configuration_version as current_host_configuration_version,
    a.memory_buffered_kb as memory_buffered_kb,
    a.memory_cached_kb as memory_cached_kb,
    a.max_memory_buffered_kb as max_memory_buffered_kb,
    a.max_memory_cached_kb as max_memory_cached_kb
FROM     vm_daily_history as a
        LEFT OUTER JOIN vm_disks_usage_daily_history as b
            ON (a.history_datetime = b.history_datetime AND a.vm_id = b.vm_id);

CREATE OR REPLACE VIEW v4_0_statistics_vms_users_usage_hourly
 AS
SELECT history_id,
       history_datetime,
       user_id,
       vm_id,
       session_time_in_minutes,
       cpu_usage_percent,
       max_cpu_usage,
       memory_usage_percent,
       max_memory_usage,
       user_cpu_usage_percent,
       max_user_cpu_usage_percent,
       system_cpu_usage_percent,
       max_system_cpu_usage_percent,
       vm_ip,
       vm_client_ip,
       user_logged_in_to_guest,
       currently_running_on_host,
       vm_configuration_version,
       current_host_configuration_version
FROM statistics_vms_users_usage_hourly;

CREATE OR REPLACE VIEW v4_0_statistics_vms_users_usage_daily
 AS
SELECT history_id,
       history_datetime,
       user_id,
       vm_id,
       session_time_in_minutes,
       cpu_usage_percent,
       max_cpu_usage,
       memory_usage_percent,
       max_memory_usage,
       user_cpu_usage_percent,
       max_user_cpu_usage_percent,
       system_cpu_usage_percent,
       max_system_cpu_usage_percent,
       vm_ip,
       vm_client_ip,
       user_logged_in_to_guest,
       currently_running_on_host,
       vm_configuration_version,
       current_host_configuration_version
FROM statistics_vms_users_usage_daily;

CREATE OR REPLACE VIEW v4_0_configuration_history_vms_interfaces
 AS
SELECT
      history_id as history_id,
      vm_interface_id as vm_interface_id,
      vm_interface_name as vm_interface_name,
      vm_interface_type as vm_interface_type,
      vm_interface_speed_bps as vm_interface_speed_bps,
      mac_address as mac_address,
      logical_network_name,
      vm_configuration_version as vm_configuration_version,
      create_date as create_date,
      update_date as update_date,
      delete_date as delete_date
FROM vm_interface_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_vms_interfaces
 AS
SELECT
      history_id as history_id,
      vm_interface_id as vm_interface_id,
      vm_interface_name as vm_interface_name,
      vm_interface_type as vm_interface_type,
      vm_interface_speed_bps as vm_interface_speed_bps,
      mac_address as mac_address,
      logical_network_name,
      vm_configuration_version as vm_configuration_version,
      create_date as create_date,
      update_date as update_date
FROM vm_interface_configuration
WHERE history_id in (SELECT max(a.history_id) FROM vm_interface_configuration as a GROUP BY a.vm_interface_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_vms_interfaces_resources_usage_samples
 AS

SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      vm_interface_id as vm_interface_id,
      receive_rate_percent as receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      vm_interface_configuration_version as vm_interface_configuration_version
FROM vm_interface_samples_history;

CREATE OR REPLACE VIEW v4_0_statistics_vms_interfaces_resources_usage_hourly
 AS

SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      vm_interface_id as vm_interface_id,
      receive_rate_percent as receive_rate_percent,
      max_receive_rate_percent as max_receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      max_transmit_rate_percent as max_transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      vm_interface_configuration_version as vm_interface_configuration_version
FROM vm_interface_hourly_history;

CREATE OR REPLACE VIEW v4_0_statistics_vms_interfaces_resources_usage_daily
 AS

SELECT
      history_id as history_id,
      history_datetime as history_datetime,
      vm_interface_id as vm_interface_id,
      receive_rate_percent as receive_rate_percent,
      max_receive_rate_percent as max_receive_rate_percent,
      transmit_rate_percent as transmit_rate_percent,
      max_transmit_rate_percent as max_transmit_rate_percent,
      received_total_byte as received_total_byte,
      transmitted_total_byte as transmitted_total_byte,
      vm_interface_configuration_version as vm_interface_configuration_version
FROM vm_interface_daily_history;

CREATE OR REPLACE VIEW v4_0_configuration_history_vms_disks
 AS
SELECT
    history_id as history_id,
    vm_disk_id as vm_disk_id,
    CASE
          WHEN vm_disk_name IS NOT NULL THEN vm_disk_name
          ELSE 'disk ' || cast(vm_internal_drive_mapping as varchar)
    END as vm_disk_name,
    vm_disk_description as vm_disk_description,
    cast(NULL as uuid) as image_id,
    storage_domain_id as storage_domain_id,
    vm_disk_size_mb as vm_disk_size_mb,
    vm_disk_type as vm_disk_type,
    vm_disk_format as vm_disk_format,
    is_shared as is_shared,
    create_date as create_date,
    update_date as update_date,
    delete_date as delete_date
FROM vm_disk_configuration;

CREATE OR REPLACE VIEW v4_0_latest_configuration_vms_disks
 AS
SELECT
    history_id as history_id,
    vm_disk_id as vm_disk_id,
    CASE
          WHEN vm_disk_name IS NOT NULL THEN vm_disk_name
          ELSE 'disk ' || cast(vm_internal_drive_mapping as varchar)
    END as vm_disk_name,
    vm_disk_description as vm_disk_description,
    cast(NULL as uuid) as image_id,
    storage_domain_id as storage_domain_id,
    vm_disk_size_mb as vm_disk_size_mb,
    vm_disk_type as vm_disk_type,
    vm_disk_format as vm_disk_format,
    is_shared as is_shared,
    create_date as create_date,
    update_date as update_date
FROM vm_disk_configuration
WHERE history_id in (SELECT max(a.history_id) FROM vm_disk_configuration as a GROUP BY a.vm_disk_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_statistics_vms_disks_resources_usage_samples
 AS
SELECT
    history_id as history_id,
    history_datetime as history_datetime,
    vm_disk_id as vm_disk_id,
    vm_disk_status as vm_disk_status,
    seconds_in_status as seconds_in_status,
    cast(seconds_in_status as numeric(7,2)) / 60 as minutes_in_status,
    vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    read_rate_bytes_per_second as read_rate_bytes_per_second,
    read_latency_seconds as read_latency_seconds,
    write_rate_bytes_per_second as write_rate_bytes_per_second,
    write_latency_seconds as write_latency_seconds,
    flush_latency_seconds as flush_latency_seconds,
    vm_disk_configuration_version as vm_disk_configuration_version
FROM vm_disk_samples_history;

CREATE OR REPLACE VIEW v4_0_statistics_vms_disks_resources_usage_hourly
 AS
SELECT
    history_id as history_id,
    history_datetime as history_datetime,
    vm_disk_id as vm_disk_id,
    vm_disk_status as vm_disk_status,
    cast(minutes_in_status * 60 as integer) as seconds_in_status,
    minutes_in_status as minutes_in_status,
    vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    read_rate_bytes_per_second as read_rate_bytes_per_second,
    max_read_rate_bytes_per_second as max_read_rate_bytes_per_second,
    read_latency_seconds as read_latency_seconds,
    max_read_latency_seconds as max_read_latency_seconds,
    write_rate_bytes_per_second as write_rate_bytes_per_second,
    max_write_rate_bytes_per_second as max_write_rate_bytes_per_second,
    write_latency_seconds as write_latency_seconds,
    max_write_latency_seconds as max_write_latency_seconds,
    flush_latency_seconds as flush_latency_seconds,
    max_flush_latency_seconds as max_flush_latency_seconds,
    vm_disk_configuration_version as vm_disk_configuration_version
FROM vm_disk_hourly_history;

CREATE OR REPLACE VIEW v4_0_statistics_vms_disks_resources_usage_daily
 AS
SELECT
    history_id as history_id,
    history_datetime as history_datetime,
    vm_disk_id as vm_disk_id,
    vm_disk_status as vm_disk_status,
    cast(minutes_in_status * 60 as integer) as seconds_in_status,
    minutes_in_status as minutes_in_status,
    vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    read_rate_bytes_per_second as read_rate_bytes_per_second,
    max_read_rate_bytes_per_second as max_read_rate_bytes_per_second,
    read_latency_seconds as read_latency_seconds,
    max_read_latency_seconds as max_read_latency_seconds,
    write_rate_bytes_per_second as write_rate_bytes_per_second,
    max_write_rate_bytes_per_second as max_write_rate_bytes_per_second,
    write_latency_seconds as write_latency_seconds,
    max_write_latency_seconds as max_write_latency_seconds,
    flush_latency_seconds as flush_latency_seconds,
    max_flush_latency_seconds as max_flush_latency_seconds,
    vm_disk_configuration_version as vm_disk_configuration_version
FROM vm_disk_daily_history;

CREATE OR REPLACE VIEW v4_0_configuration_history_vms_devices
 AS
SELECT
    history_id as history_id,
    vm_id,
    device_id,
    type,
    address,
    is_managed,
    is_plugged,
    is_readonly,
    vm_configuration_version,
    device_configuration_version,
    create_date,
    update_date,
    delete_date
FROM vm_device_history;

CREATE OR REPLACE VIEW v4_0_latest_configuration_vms_devices
 AS
SELECT
    history_id as history_id,
    vm_id,
    device_id,
    type,
    address,
    is_managed,
    is_plugged,
    is_readonly,
    vm_configuration_version,
    device_configuration_version,
    create_date,
    update_date
FROM vm_device_history
WHERE history_id in (SELECT max(a.history_id) FROM vm_device_history as a GROUP BY a.vm_id, a.device_id)
      and delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_vms_resources_usage_samples
 AS
 SELECT
    conf.vm_id as vm_id,
    conf.vm_name as vm_name,
    conf.vm_description as vm_description,
    conf.vm_type as vm_type,
    conf.cluster_id as cluster_id,
    conf.template_id as template_id,
    conf.template_name as template_name,
    conf.cpu_per_socket as cpu_per_socket,
    conf.number_of_sockets as number_of_sockets,
    conf.memory_size_mb as memory_size_mb,
    conf.operating_system as operating_system,
    conf.default_host as default_host,
    conf.high_availability as high_availability,
    conf.initialized as initialized,
    conf.stateless as stateless,
    conf.fail_back as fail_back,
    conf.usb_policy as usb_policy,
    conf.time_zone as time_zone,
    conf.vm_pool_id as vm_pool_id,
    conf.vm_pool_name as vm_pool_name,
    conf.created_by_user_id as created_by_user_id,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.default_host_configuration_version as default_host_configuration_version,
    conf.create_date as vm_create_date,
    conf.update_date as vm_update_date,
    conf.delete_date as vm_delete_date,
    stats.history_datetime as history_datetime,
    stats.vm_status as vm_status,
    stats.seconds_in_status as seconds_in_status,
    cast(stats.seconds_in_status as numeric(7,2)) / 60 as minutes_in_status,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.memory_usage_percent as memory_usage_percent,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.vm_ip as vm_ip,
    stats.vm_client_ip as vm_client_ip,
    stats.currently_running_on_host as currently_running_on_host,
    stats.current_user_id as current_user_id,
    stats.user_logged_in_to_guest,
    stats.disks_usage as disks_usage,
    stats.current_host_configuration_version as current_host_configuration_version,
    stats.memory_buffered_kb as memory_buffered_kb,
    stats.memory_cached_kb as memory_cached_kb,
    device_conf.device_id as device_id,
    device_conf.type as device_type,
    device_conf.address as address,
    device_conf.is_managed as is_managed,
    device_conf.is_plugged as is_plugged,
    device_conf.is_readonly as is_readonly,
    device_conf.create_date as device_create_date,
    device_conf.update_date as device_update_date,
    device_conf.delete_date as device_delete_date,
    nic_conf.vm_interface_id as vm_interface_id,
    nic_conf.vm_interface_name as vm_interface_name,
    nic_conf.vm_interface_type as vm_interface_type,
    nic_conf.vm_interface_speed_bps as vm_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name as logical_network_name,
    nic_conf.create_date as vm_interface_create_date,
    nic_conf.update_date as vm_interface_update_date,
    nic_conf.delete_date as vm_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte,
    disk_conf.vm_disk_id as vm_disk_id,
    disk_conf.vm_disk_name as vm_disk_name,
    disk_conf.vm_disk_description as vm_disk_description,
    cast(NULL as uuid) as image_id,
    disk_conf.storage_domain_id as storage_domain_id,
    disk_conf.vm_disk_size_mb as vm_disk_size_mb,
    disk_conf.vm_disk_type as vm_disk_type,
    disk_conf.vm_disk_format as vm_disk_format,
    disk_conf.is_shared as is_shared,
    disk_conf.create_date as vm_disk_create_date,
    disk_conf.update_date as vm_disk_update_date,
    disk_conf.delete_date as vm_disk_delete_date,
    disk_stats.vm_disk_status as vm_disk_status,
    disk_stats.seconds_in_status as vm_disk_seconds_in_status,
    cast(disk_stats.seconds_in_status as numeric(7,2)) / 60 as vm_disk_minutes_in_status,
    disk_stats.vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    disk_stats.read_rate_bytes_per_second as read_rate_bytes_per_second,
    disk_stats.read_latency_seconds as read_latency_seconds,
    disk_stats.write_rate_bytes_per_second as write_rate_bytes_per_second,
    disk_stats.write_latency_seconds as write_latency_seconds,
    disk_stats.flush_latency_seconds as flush_latency_seconds
FROM v4_0_configuration_history_vms AS conf
    LEFT OUTER JOIN v4_0_statistics_vms_resources_usage_samples AS stats
        ON (conf.history_id = stats.vm_configuration_version)
    LEFT OUTER JOIN  v4_0_configuration_history_vms_devices device_conf
        ON (conf.history_id = device_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_vms_disks disk_conf
        ON (device_conf.device_configuration_version = disk_conf.history_id)
    LEFT OUTER JOIN v4_0_configuration_history_vms_interfaces AS nic_conf
        ON (device_conf.device_configuration_version = nic_conf.history_id  AND
            conf.history_id = nic_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_vms_interfaces_resources_usage_samples AS nic_stats
        ON (nic_conf.history_id = nic_stats.vm_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime)
    LEFT OUTER JOIN v4_0_statistics_vms_disks_resources_usage_samples disk_stats
        ON (disk_conf.history_id = disk_stats.vm_disk_configuration_version AND
            stats.history_datetime = disk_stats.history_datetime);

CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_vms_resources_usage_hourly
 AS
 SELECT
    conf.vm_id as vm_id,
    conf.vm_name as vm_name,
    conf.vm_description as vm_description,
    conf.vm_type as vm_type,
    conf.cluster_id as cluster_id,
    conf.template_id as template_id,
    conf.template_name as template_name,
    conf.cpu_per_socket as cpu_per_socket,
    conf.number_of_sockets as number_of_sockets,
    conf.memory_size_mb as memory_size_mb,
    conf.operating_system as operating_system,
    conf.default_host as default_host,
    conf.high_availability as high_availability,
    conf.initialized as initialized,
    conf.stateless as stateless,
    conf.fail_back as fail_back,
    conf.usb_policy as usb_policy,
    conf.time_zone as time_zone,
    conf.vm_pool_id as vm_pool_id,
    conf.vm_pool_name as vm_pool_name,
    conf.created_by_user_id as created_by_user_id,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.default_host_configuration_version as default_host_configuration_version,
    conf.create_date as vm_create_date,
    conf.update_date as vm_update_date,
    conf.delete_date as vm_delete_date,
    stats.history_datetime as history_datetime,
    stats.vm_status as vm_status,
    cast(stats.minutes_in_status * 60 as integer) as vm_seconds_in_status,
    stats.minutes_in_status as vm_minutes_in_status,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.max_cpu_usage as max_cpu_usage,
    stats.memory_usage_percent as memory_usage_percent,
    stats.max_memory_usage as max_memory_usage,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    stats.vm_ip as vm_ip,
    stats.currently_running_on_host as currently_running_on_host,
    stats.current_user_id as current_user_id,
    stats.disks_usage as disks_usage,
    stats.current_host_configuration_version as current_host_configuration_version,
    stats.memory_buffered_kb as memory_buffered_kb,
    stats.memory_cached_kb as memory_cached_kb,
    stats.max_memory_buffered_kb as max_memory_buffered_kb,
    stats.max_memory_cached_kb as max_memory_cached_kb,
    device_conf.device_id as device_id,
    device_conf.type as device_type,
    device_conf.address as address,
    device_conf.is_managed as is_managed,
    device_conf.is_plugged as is_plugged,
    device_conf.is_readonly as is_readonly,
    device_conf.create_date as device_create_date,
    device_conf.update_date as device_update_date,
    device_conf.delete_date as device_delete_date,
    nic_conf.vm_interface_id as vm_interface_id,
    nic_conf.vm_interface_name as vm_interface_name,
    nic_conf.vm_interface_type as vm_interface_type,
    nic_conf.vm_interface_speed_bps as vm_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name as logical_network_name,
    nic_conf.create_date as vm_interface_create_date,
    nic_conf.update_date as vm_interface_update_date,
    nic_conf.delete_date as vm_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.max_receive_rate_percent as max_receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.max_transmit_rate_percent as max_transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte,
    disk_conf.vm_disk_id as vm_disk_id,
    disk_conf.vm_disk_name as vm_disk_name,
    disk_conf.vm_disk_description as vm_disk_description,
    cast(NULL as uuid) as image_id,
    disk_conf.storage_domain_id as storage_domain_id,
    disk_conf.vm_disk_size_mb as vm_disk_size_mb,
    disk_conf.vm_disk_type as vm_disk_type,
    disk_conf.vm_disk_format as vm_disk_format,
    disk_conf.is_shared as is_shared,
    disk_conf.create_date as vm_disk_create_date,
    disk_conf.update_date as vm_disk_update_date,
    disk_conf.delete_date as vm_disk_delete_date,
    disk_stats.vm_disk_status as vm_disk_status,
    cast(disk_stats.minutes_in_status * 60 as integer) as vm_disk_seconds_in_status,
    disk_stats.minutes_in_status as vm_disk_minutes_in_status,
    disk_stats.vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    disk_stats.read_rate_bytes_per_second as read_rate_bytes_per_second,
    disk_stats.max_read_rate_bytes_per_second as max_read_rate_bytes_per_second,
    disk_stats.read_latency_seconds as read_latency_seconds,
    disk_stats.max_read_latency_seconds as max_read_latency_seconds,
    disk_stats.write_rate_bytes_per_second as write_rate_bytes_per_second,
    disk_stats.max_write_rate_bytes_per_second as max_write_rate_bytes_per_second,
    disk_stats.write_latency_seconds as write_latency_seconds,
    disk_stats.max_write_latency_seconds as max_write_latency_seconds,
    disk_stats.flush_latency_seconds as flush_latency_seconds,
    disk_stats.max_flush_latency_seconds as max_flush_latency_seconds
FROM v4_0_configuration_history_vms AS conf
    LEFT OUTER JOIN v4_0_statistics_vms_resources_usage_hourly AS stats
        ON (conf.history_id = stats.vm_configuration_version)
    LEFT OUTER JOIN  v4_0_configuration_history_vms_devices device_conf
        ON (conf.history_id = device_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_vms_disks disk_conf
        ON (device_conf.device_configuration_version = disk_conf.history_id)
    LEFT OUTER JOIN v4_0_configuration_history_vms_interfaces AS nic_conf
        ON (device_conf.device_configuration_version = nic_conf.history_id  AND
            conf.history_id = nic_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_vms_interfaces_resources_usage_hourly AS nic_stats
        ON (nic_conf.history_id = nic_stats.vm_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime)
    LEFT OUTER JOIN v4_0_statistics_vms_disks_resources_usage_hourly disk_stats
        ON (disk_conf.history_id = disk_stats.vm_disk_configuration_version AND
            stats.history_datetime = disk_stats.history_datetime);


CREATE OR REPLACE VIEW v4_0_fully_joined_statistics_vms_resources_usage_daily
 AS
 SELECT
    conf.vm_id as vm_id,
    conf.vm_name as vm_name,
    conf.vm_description as vm_description,
    conf.vm_type as vm_type,
    conf.cluster_id as cluster_id,
    conf.template_id as template_id,
    conf.template_name as template_name,
    conf.cpu_per_socket as cpu_per_socket,
    conf.number_of_sockets as number_of_sockets,
    conf.memory_size_mb as memory_size_mb,
    conf.operating_system as operating_system,
    conf.default_host as default_host,
    conf.high_availability as high_availability,
    conf.initialized as initialized,
    conf.stateless as stateless,
    conf.fail_back as fail_back,
    conf.usb_policy as usb_policy,
    conf.time_zone as time_zone,
    conf.vm_pool_id as vm_pool_id,
    conf.vm_pool_name as vm_pool_name,
    conf.created_by_user_id as created_by_user_id,
    conf.cluster_configuration_version as cluster_configuration_version,
    conf.default_host_configuration_version as default_host_configuration_version,
    conf.create_date as vm_create_date,
    conf.update_date as vm_update_date,
    conf.delete_date as vm_delete_date,
    stats.history_datetime as history_datetime,
    stats.vm_status as vm_status,
    cast(stats.minutes_in_status * 60 as integer) as vm_seconds_in_status,
    stats.minutes_in_status as vm_minutes_in_status,
    stats.cpu_usage_percent as cpu_usage_percent,
    stats.max_cpu_usage as max_cpu_usage,
    stats.memory_usage_percent as memory_usage_percent,
    stats.max_memory_usage as max_memory_usage,
    stats.user_cpu_usage_percent as user_cpu_usage_percent,
    stats.max_user_cpu_usage_percent as max_user_cpu_usage_percent,
    stats.system_cpu_usage_percent as system_cpu_usage_percent,
    stats.max_system_cpu_usage_percent as max_system_cpu_usage_percent,
    stats.vm_ip as vm_ip,
    stats.currently_running_on_host as currently_running_on_host,
    stats.current_user_id as current_user_id,
    stats.disks_usage as disks_usage,
    stats.current_host_configuration_version as current_host_configuration_version,
    stats.memory_buffered_kb as memory_buffered_kb,
    stats.memory_cached_kb as memory_cached_kb,
    stats.max_memory_buffered_kb as max_memory_buffered_kb,
    stats.max_memory_cached_kb as max_memory_cached_kb,
    device_conf.device_id as device_id,
    device_conf.type as device_type,
    device_conf.address as address,
    device_conf.is_managed as is_managed,
    device_conf.is_plugged as is_plugged,
    device_conf.is_readonly as is_readonly,
    device_conf.create_date as device_create_date,
    device_conf.update_date as device_update_date,
    device_conf.delete_date as device_delete_date,
    nic_conf.vm_interface_id as vm_interface_id,
    nic_conf.vm_interface_name as vm_interface_name,
    nic_conf.vm_interface_type as vm_interface_type,
    nic_conf.vm_interface_speed_bps as vm_interface_speed_bps,
    nic_conf.mac_address as mac_address,
    nic_conf.logical_network_name as logical_network_name,
    nic_conf.create_date as vm_interface_create_date,
    nic_conf.update_date as vm_interface_update_date,
    nic_conf.delete_date as vm_interface_delete_date,
    nic_stats.receive_rate_percent as receive_rate_percent,
    nic_stats.max_receive_rate_percent as max_receive_rate_percent,
    nic_stats.transmit_rate_percent as transmit_rate_percent,
    nic_stats.max_transmit_rate_percent as max_transmit_rate_percent,
    nic_stats.received_total_byte as received_total_byte,
    nic_stats.transmitted_total_byte as transmitted_total_byte,
    disk_conf.vm_disk_id as vm_disk_id,
    disk_conf.vm_disk_name as vm_disk_name,
    disk_conf.vm_disk_description as vm_disk_description,
    cast(NULL as uuid) as image_id,
    disk_conf.storage_domain_id as storage_domain_id,
    disk_conf.vm_disk_size_mb as vm_disk_size_mb,
    disk_conf.vm_disk_type as vm_disk_type,
    disk_conf.vm_disk_format as vm_disk_format,
    disk_conf.is_shared as is_shared,
    disk_conf.create_date as vm_disk_create_date,
    disk_conf.update_date as vm_disk_update_date,
    disk_conf.delete_date as vm_disk_delete_date,
    disk_stats.vm_disk_status as vm_disk_status,
    cast(disk_stats.minutes_in_status * 60 as integer) as vm_disk_seconds_in_status,
    disk_stats.minutes_in_status as vm_disk_minutes_in_status,
    disk_stats.vm_disk_actual_size_mb as vm_disk_actual_size_mb,
    disk_stats.read_rate_bytes_per_second as read_rate_bytes_per_second,
    disk_stats.max_read_rate_bytes_per_second as max_read_rate_bytes_per_second,
    disk_stats.read_latency_seconds as read_latency_seconds,
    disk_stats.max_read_latency_seconds as max_read_latency_seconds,
    disk_stats.write_rate_bytes_per_second as write_rate_bytes_per_second,
    disk_stats.max_write_rate_bytes_per_second as max_write_rate_bytes_per_second,
    disk_stats.write_latency_seconds as write_latency_seconds,
    disk_stats.max_write_latency_seconds as max_write_latency_seconds,
    disk_stats.flush_latency_seconds as flush_latency_seconds,
    disk_stats.max_flush_latency_seconds as max_flush_latency_seconds
FROM v4_0_configuration_history_vms AS conf
    LEFT OUTER JOIN v4_0_statistics_vms_resources_usage_daily AS stats
        ON (conf.history_id = stats.vm_configuration_version)
    LEFT OUTER JOIN  v4_0_configuration_history_vms_devices device_conf
        ON (conf.history_id = device_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_configuration_history_vms_disks disk_conf
        ON (device_conf.device_configuration_version = disk_conf.history_id)
    LEFT OUTER JOIN v4_0_configuration_history_vms_interfaces AS nic_conf
        ON (device_conf.device_configuration_version = nic_conf.history_id  AND
            conf.history_id = nic_conf.vm_configuration_version)
    LEFT OUTER JOIN v4_0_statistics_vms_interfaces_resources_usage_daily AS nic_stats
        ON (nic_conf.history_id = nic_stats.vm_interface_configuration_version AND
            stats.history_datetime = nic_stats.history_datetime)
    LEFT OUTER JOIN v4_0_statistics_vms_disks_resources_usage_daily disk_stats
        ON (disk_conf.history_id = disk_stats.vm_disk_configuration_version AND
            stats.history_datetime = disk_stats.history_datetime);

CREATE OR REPLACE VIEW v4_0_users_details_history
 AS
SELECT
      user_id,
      first_name,
      last_name,
      domain,
      username,
      department,
      user_role_title,
      email,
      external_id,
      active,
      create_date,
      update_date,
      delete_date
FROM users_details_history;

CREATE OR REPLACE VIEW v4_0_latest_users_details
 AS
SELECT
      user_id,
      first_name,
      last_name,
      domain,
      username,
      department,
      user_role_title,
      email,
      external_id,
      active,
      create_date,
      update_date,
      delete_date
FROM users_details_history
WHERE delete_date IS NULL;

CREATE OR REPLACE VIEW v4_0_tags_relations_history
 AS
SELECT    history_id as history_id,
        entity_id as entity_id,
        entity_type as entity_type,
        parent_id as parent_id,
        attach_date as attach_date,
        detach_date as detach_date
FROM         tag_relations_history
WHERE       entity_type in(3,2,5,18,15);

CREATE OR REPLACE VIEW v4_0_latest_tags_relations
 AS
SELECT    history_id as history_id,
        entity_id as entity_id,
        entity_type as entity_type,
        parent_id as parent_id,
        attach_date as attach_date,
        detach_date as detach_date
FROM         tag_relations_history
WHERE       entity_type in(3,2,5,18,15)
       and history_id in (SELECT max(a.history_id) FROM tag_relations_history as a GROUP BY a.entity_id, a.parent_id)
       and detach_date IS NULL;

CREATE OR REPLACE VIEW v4_0_tags_details_history
 AS
SELECT  history_id as history_id,
        tag_id as tag_id,
        tag_name as tag_name,
        tag_description as tag_description,
        tag_path as tag_path,
        tag_level as tag_level,
        create_date as create_date,
        update_date as update_date,
        delete_date as delete_date
FROM         tag_details;

CREATE OR REPLACE VIEW v4_0_latest_tags_details
 AS
SELECT  history_id as history_id,
        tag_id as tag_id,
        tag_name as tag_name,
        tag_description as tag_description,
        tag_path as tag_path,
        tag_level as tag_level,
        create_date as create_date,
        update_date as update_date,
        delete_date as delete_date
FROM         tag_details
WHERE history_id in (SELECT max(a.history_id) FROM tag_details as a GROUP BY a.tag_id)
      and delete_date IS NULL;
