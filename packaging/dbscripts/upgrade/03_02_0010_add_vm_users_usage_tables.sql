CREATE SEQUENCE statistics_vms_users_usage_hourly_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE statistics_vms_users_usage_hourly
(
   history_id INTEGER DEFAULT NEXTVAL('statistics_vms_users_usage_hourly_seq') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   user_name VARCHAR(255),
   vm_id UUID NOT NULL,
   session_time_in_minutes DECIMAL(7,2) NOT NULL DEFAULT 1,
   cpu_usage_percent SMALLINT  DEFAULT 0,
   max_cpu_usage SMALLINT,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   vm_ip VARCHAR(255),
   currently_running_on_host UUID,
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   current_host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_users_usage_history_datetime_hourly ON statistics_vms_users_usage_hourly (history_datetime);
CREATE INDEX IDX_vm_users_usage_configuration_version_hourly ON statistics_vms_users_usage_hourly (vm_configuration_version);
CREATE INDEX IDX_vm_users_usage_current_host_configuration_hourly ON statistics_vms_users_usage_hourly (current_host_configuration_version);

CREATE SEQUENCE statistics_vms_users_usage_daily_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE statistics_vms_users_usage_daily
(
   history_id INTEGER DEFAULT NEXTVAL('statistics_vms_users_usage_daily_seq') primary key NOT NULL,
   history_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
   user_name VARCHAR(255),
   vm_id UUID NOT NULL,
   session_time_in_minutes DECIMAL(7,2) NOT NULL DEFAULT 1,
   cpu_usage_percent SMALLINT  DEFAULT 0,
   max_cpu_usage SMALLINT,
   memory_usage_percent SMALLINT  DEFAULT 0,
   max_memory_usage SMALLINT,
   user_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_user_cpu_usage_percent SMALLINT  DEFAULT 0,
   system_cpu_usage_percent SMALLINT  DEFAULT 0,
   max_system_cpu_usage_percent SMALLINT  DEFAULT 0,
   vm_ip VARCHAR(255),
   currently_running_on_host UUID,
   vm_configuration_version INTEGER REFERENCES vm_configuration (history_id),
   current_host_configuration_version INTEGER REFERENCES host_configuration (history_id)
) WITH OIDS;

CREATE INDEX IDX_vm_users_usage_history_datetime_daily ON statistics_vms_users_usage_daily (history_datetime);
CREATE INDEX IDX_vm_users_usage_configuration_version_daily ON statistics_vms_users_usage_daily (vm_configuration_version);
CREATE INDEX IDX_vm_users_usage_current_host_configuration_daily ON statistics_vms_users_usage_daily (current_host_configuration_version);

