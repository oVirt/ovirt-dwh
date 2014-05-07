-- Bug-Url: https://bugzilla.redhat.com/1078897
-- Updated retroactivly user and system cpu usage percent,
-- according to the number of cpus of the vm.

-- add temp columns for hourly sys and user cpu usage percent
SELECT fn_db_add_column('statistics_vms_users_usage_hourly', 'user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_hourly', 'max_user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_hourly', 'system_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_hourly', 'max_system_cpu_usage_percent_temp', 'smallint');

--update hourly values of user and sys cpu_usage_percent, avg and max, according to number of cpu's
CREATE OR REPLACE function __temp_hourly_cpu_usage_percent() RETURNS void
AS $function$
BEGIN
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'statistics_vms_users_usage_hourly'
                AND column_name ilike 'user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_hourly'
                    AND column_name ilike 'max_user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_hourly'
                    AND column_name ilike 'system_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_hourly'
                    AND column_name ilike 'max_system_cpu_usage_percent_temp'
        )
    )
        THEN
            BEGIN
                UPDATE statistics_vms_users_usage_hourly
                SET user_cpu_usage_percent_temp =
                    statistics_vms_users_usage_hourly.user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_user_cpu_usage_percent_temp =
                    statistics_vms_users_usage_hourly.max_user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    system_cpu_usage_percent_temp =
                    statistics_vms_users_usage_hourly.system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_system_cpu_usage_percent_temp =
                    statistics_vms_users_usage_hourly.max_system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket )
                FROM vm_configuration
                WHERE
                    statistics_vms_users_usage_hourly.vm_id =
                    vm_configuration.vm_id
                    AND statistics_vms_users_usage_hourly.vm_configuration_version =
                    vm_configuration.history_id;
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_hourly_cpu_usage_percent();

DROP function __temp_hourly_cpu_usage_percent();

--delete user and sys cpu_usage_percent columns from statistics_vms_users_usage_hourly table
SELECT fn_db_drop_column('statistics_vms_users_usage_hourly', 'user_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_hourly', 'max_user_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_hourly', 'system_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_hourly', 'max_system_cpu_usage_percent');

--change columns names from temp to the names of the dropped columns
ALTER TABLE  statistics_vms_users_usage_hourly RENAME COLUMN user_cpu_usage_percent_temp TO user_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_hourly RENAME COLUMN max_user_cpu_usage_percent_temp TO max_user_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_hourly RENAME COLUMN system_cpu_usage_percent_temp TO system_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_hourly RENAME COLUMN max_system_cpu_usage_percent_temp TO max_system_cpu_usage_percent;

-- add temp columns for daily sys and user cpu usage percent
SELECT fn_db_add_column('statistics_vms_users_usage_daily', 'user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_daily', 'max_user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_daily', 'system_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('statistics_vms_users_usage_daily', 'max_system_cpu_usage_percent_temp', 'smallint');

--update daily values of user and sys cpu_usage_percent, avg and max, according to number of cpu's.
CREATE OR REPLACE function __temp_daily_cpu_usage_percent() RETURNS void
AS $function$
BEGIN
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'statistics_vms_users_usage_daily'
                AND column_name ilike 'user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_daily'
                    AND column_name ilike 'max_user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_daily'
                    AND column_name ilike 'system_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'statistics_vms_users_usage_daily'
                    AND column_name ilike 'max_system_cpu_usage_percent_temp'
        )
    )
        THEN
            BEGIN
                UPDATE statistics_vms_users_usage_daily
                SET user_cpu_usage_percent_temp =
                    statistics_vms_users_usage_daily.user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_user_cpu_usage_percent_temp =
                    statistics_vms_users_usage_daily.max_user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    system_cpu_usage_percent_temp =
                    statistics_vms_users_usage_daily.system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_system_cpu_usage_percent_temp =
                    statistics_vms_users_usage_daily.max_system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket )
                FROM vm_configuration
                WHERE
                    statistics_vms_users_usage_daily.vm_id =
                    vm_configuration.vm_id
                    AND statistics_vms_users_usage_daily.vm_configuration_version =
                    vm_configuration.history_id;
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_daily_cpu_usage_percent();

DROP function __temp_daily_cpu_usage_percent();

--delete user and sys cpu_usage_percent columns from statistics_vms_users_usage_daily table
SELECT fn_db_drop_column('statistics_vms_users_usage_daily', 'user_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_daily', 'max_user_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_daily', 'system_cpu_usage_percent');
SELECT fn_db_drop_column('statistics_vms_users_usage_daily', 'max_system_cpu_usage_percent');

--change columns names from temp to the names of the dropped columns
ALTER TABLE  statistics_vms_users_usage_daily RENAME COLUMN user_cpu_usage_percent_temp TO user_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_daily RENAME COLUMN max_user_cpu_usage_percent_temp TO max_user_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_daily RENAME COLUMN system_cpu_usage_percent_temp TO system_cpu_usage_percent;
ALTER TABLE  statistics_vms_users_usage_daily RENAME COLUMN max_system_cpu_usage_percent_temp TO max_system_cpu_usage_percent;

-- add temp columns for hourly sys and user cpu usage percent
SELECT fn_db_add_column('vm_samples_history', 'user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_samples_history', 'system_cpu_usage_percent_temp', 'smallint');

--update samples values of user and sys cpu_usage_percent, avg and max, according to number of cpu's
CREATE OR REPLACE function __temp_vm_samples_history() RETURNS void
AS $function$
BEGIN
if (
    EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name ilike 'vm_samples_history'
            AND column_name ilike 'user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_samples_history'
                    AND column_name ilike 'system_cpu_usage_percent_temp'
        )
    )
        THEN
            BEGIN
                UPDATE vm_samples_history
                SET user_cpu_usage_percent_temp =
                    vm_samples_history.user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    system_cpu_usage_percent_temp =
                    vm_samples_history.system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket )
                FROM vm_configuration
                WHERE
                    vm_samples_history.vm_id =
                    vm_configuration.vm_id
                    AND vm_samples_history.vm_configuration_version =
                    vm_configuration.history_id;
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_vm_samples_history();

DROP function __temp_vm_samples_history();

--delete user and sys cpu_usage_percent columns from vm_samples_history table
SELECT fn_db_drop_column('vm_samples_history', 'user_cpu_usage_percent');
SELECT fn_db_drop_column('vm_samples_history', 'system_cpu_usage_percent');

--change columns names from temp to the names of the dropped columns
ALTER TABLE  vm_samples_history RENAME COLUMN user_cpu_usage_percent_temp TO user_cpu_usage_percent;
ALTER TABLE  vm_samples_history RENAME COLUMN system_cpu_usage_percent_temp TO system_cpu_usage_percent;

-- add temp columns for hourly sys and user cpu usage percent
SELECT fn_db_add_column('vm_hourly_history', 'user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_hourly_history', 'max_user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_hourly_history', 'system_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_hourly_history', 'max_system_cpu_usage_percent_temp', 'smallint');

--update hourly values of user and sys cpu_usage_percent according to number of cpu's
CREATE OR REPLACE function __temp_vm_hourly_history() RETURNS void
AS $function$
BEGIN
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'vm_hourly_history'
                AND column_name ilike 'user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_hourly_history'
                    AND column_name ilike 'max_user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_hourly_history'
                    AND column_name ilike 'system_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_hourly_history'
                    AND column_name ilike 'max_system_cpu_usage_percent_temp'
        )
    )
        THEN
            BEGIN
                UPDATE vm_hourly_history
                SET user_cpu_usage_percent_temp =
                    vm_hourly_history.user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_user_cpu_usage_percent_temp =
                    vm_hourly_history.max_user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    system_cpu_usage_percent_temp =
                    vm_hourly_history.system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_system_cpu_usage_percent_temp =
                    vm_hourly_history.max_system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket )
                FROM vm_configuration
                WHERE
                    vm_hourly_history.vm_id =
                    vm_configuration.vm_id
                    AND vm_hourly_history.vm_configuration_version =
                    vm_configuration.history_id;
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_vm_hourly_history();

DROP function __temp_vm_hourly_history();

--delete user and sys cpu_usage_percent columns from vm_hourly_history table
SELECT fn_db_drop_column('vm_hourly_history', 'user_cpu_usage_percent');
SELECT fn_db_drop_column('vm_hourly_history', 'max_user_cpu_usage_percent');
SELECT fn_db_drop_column('vm_hourly_history', 'system_cpu_usage_percent');
SELECT fn_db_drop_column('vm_hourly_history', 'max_system_cpu_usage_percent');

--change columns names from temp to the names of the dropped columns
ALTER TABLE  vm_hourly_history RENAME COLUMN user_cpu_usage_percent_temp TO user_cpu_usage_percent;
ALTER TABLE  vm_hourly_history RENAME COLUMN max_user_cpu_usage_percent_temp TO max_user_cpu_usage_percent;
ALTER TABLE  vm_hourly_history RENAME COLUMN system_cpu_usage_percent_temp TO system_cpu_usage_percent;
ALTER TABLE  vm_hourly_history RENAME COLUMN max_system_cpu_usage_percent_temp TO max_system_cpu_usage_percent;

-- add temp columns for hourly sys and user cpu usage percent
SELECT fn_db_add_column('vm_daily_history', 'user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_daily_history', 'max_user_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_daily_history', 'system_cpu_usage_percent_temp', 'smallint');
SELECT fn_db_add_column('vm_daily_history', 'max_system_cpu_usage_percent_temp', 'smallint');

--update daily values of user and sys cpu_usage_percent, avg and max, according to number of cpu's.
CREATE OR REPLACE function __temp_vm_daily_history() RETURNS void
AS $function$
BEGIN
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'vm_daily_history'
                AND column_name ilike 'user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_daily_history'
                    AND column_name ilike 'max_user_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_daily_history'
                    AND column_name ilike 'system_cpu_usage_percent_temp'
        )
        AND EXISTS (
            SELECT 1
                FROM information_schema.columns
                WHERE table_name ilike 'vm_daily_history'
                    AND column_name ilike 'max_system_cpu_usage_percent_temp'
        )
    )
        THEN
            BEGIN
                UPDATE vm_daily_history
                SET user_cpu_usage_percent_temp =
                    vm_daily_history.user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_user_cpu_usage_percent_temp =
                    vm_daily_history.max_user_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    system_cpu_usage_percent_temp =
                    vm_daily_history.system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket ),
                    max_system_cpu_usage_percent_temp =
                    vm_daily_history.max_system_cpu_usage_percent /
                    ( vm_configuration.number_of_sockets * vm_configuration.cpu_per_socket )
                FROM vm_configuration
                WHERE
                    vm_daily_history.vm_id =
                    vm_configuration.vm_id
                    AND vm_daily_history.vm_configuration_version =
                    vm_configuration.history_id;
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_vm_daily_history();

DROP function __temp_vm_daily_history();

--delete user and sys cpu_usage_percent columns from vm_daily_history table
SELECT fn_db_drop_column('vm_daily_history', 'user_cpu_usage_percent');
SELECT fn_db_drop_column('vm_daily_history', 'max_user_cpu_usage_percent');
SELECT fn_db_drop_column('vm_daily_history', 'system_cpu_usage_percent');
SELECT fn_db_drop_column('vm_daily_history', 'max_system_cpu_usage_percent');

--change columns names from temp to the names of the dropped columns
ALTER TABLE  vm_daily_history RENAME COLUMN user_cpu_usage_percent_temp TO user_cpu_usage_percent;
ALTER TABLE  vm_daily_history RENAME COLUMN max_user_cpu_usage_percent_temp TO max_user_cpu_usage_percent;
ALTER TABLE  vm_daily_history RENAME COLUMN system_cpu_usage_percent_temp TO system_cpu_usage_percent;
ALTER TABLE  vm_daily_history RENAME COLUMN max_system_cpu_usage_percent_temp TO max_system_cpu_usage_percent;
