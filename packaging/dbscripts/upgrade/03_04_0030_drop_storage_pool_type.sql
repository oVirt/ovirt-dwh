-- add is_local_storage to datacenter_configuration table
SELECT fn_db_add_column('datacenter_configuration', 'is_local_storage', 'boolean');

--update values of column is_local_storage according to historic storage_type values
create or replace function __temp_update_storage_domain_is_local_storage() returns void
as $function$
begin
	if (exists (select 1 from information_schema.columns where table_name ilike 'datacenter_configuration' and column_name ilike 'storage_type')) then
		update datacenter_configuration set is_local_storage = (storage_type = 4);
	end if;
end; $function$
language plpgsql;

select __temp_update_storage_domain_is_local_storage();

drop function __temp_update_storage_domain_is_local_storage();

--delete storage_type column from datacenter_configuration table
SELECT fn_db_drop_column('datacenter_configuration', 'storage_type');

