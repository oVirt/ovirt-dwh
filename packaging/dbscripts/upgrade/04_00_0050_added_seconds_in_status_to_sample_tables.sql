select fn_db_add_column('host_samples_history', 'seconds_in_status', 'integer NOT NULL DEFAULT 20');
select fn_db_add_column('vm_samples_history', 'seconds_in_status', 'integer NOT NULL DEFAULT 20');
select fn_db_add_column('vm_disk_samples_history', 'seconds_in_status', 'integer NOT NULL DEFAULT 20');
select fn_db_add_column('storage_domain_samples_history', 'seconds_in_status', 'integer NOT NULL DEFAULT 20');

--populate seconds_in_status values based on the value of minutes_in_status
CREATE OR REPLACE function __temp_populate_seconds_in_status() RETURNS void
AS $function$
BEGIN
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'host_samples_history'
                AND column_name ilike 'seconds_in_status'
        )
    )
        THEN
            BEGIN
                UPDATE host_samples_history
                SET seconds_in_status = cast ((minutes_in_status * 60)  as integer);
            END;
    END if;
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'vm_samples_history'
                AND column_name ilike 'seconds_in_status'
        )
    )
        THEN
            BEGIN
                UPDATE vm_samples_history
                SET seconds_in_status = cast ((minutes_in_status * 60)  as integer);
            END;
    END if;
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'vm_disk_samples_history'
                AND column_name ilike 'seconds_in_status'
        )
    )
        THEN
            BEGIN
                UPDATE vm_disk_samples_history
                SET seconds_in_status = cast ((minutes_in_status * 60)  as integer);
            END;
    END if;
    if (
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name ilike 'storage_domain_samples_history'
                AND column_name ilike 'seconds_in_status'
        )
    )
        THEN
            BEGIN
                UPDATE storage_domain_samples_history
                SET seconds_in_status = cast ((minutes_in_status * 60)  as integer);
            END;
    END if;
END; $function$
language plpgsql;

SELECT __temp_populate_seconds_in_status();

DROP function __temp_populate_seconds_in_status();

--delete minutes_in_status column from sample tables
SELECT fn_db_drop_column('host_samples_history', 'minutes_in_status');
SELECT fn_db_drop_column('vm_samples_history', 'minutes_in_status');
SELECT fn_db_drop_column('vm_disk_samples_history', 'minutes_in_status');
SELECT fn_db_drop_column('storage_domain_samples_history', 'minutes_in_status');
