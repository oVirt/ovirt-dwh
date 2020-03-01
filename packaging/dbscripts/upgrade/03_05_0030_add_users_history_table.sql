CREATE TABLE users_details_history
(
  user_id uuid primary key NOT NULL,
  first_name character varying(255),
  last_name character varying(255),
  domain character varying(255) NOT NULL,
  username character varying(255) NOT NULL,
  department character varying(255),
  user_role_title character varying(255),
  email character varying(255),
  external_id bytea NOT NULL DEFAULT ''::bytea,
  active boolean NOT NULL DEFAULT false,
  create_date TIMESTAMP WITH TIME ZONE NOT NULL,
  update_date TIMESTAMP WITH TIME ZONE,
  delete_date TIMESTAMP WITH TIME ZONE
) ;

-- vm_configuration - We can't add to vm_configuration table a FK on created_by_user_id
-- because this column already existed in the database, before we started to collect
-- users data. This mens that the created_by_user_id field may contain user_ids
-- That do not exist in the users_details_history table and we will not be able
-- to add the FK. We do not want to empty the data from the colums fopr backwards
-- compatability for users that have reports that uses this column.

SELECT fn_db_add_column('vm_samples_history', 'current_user_id', 'UUID');

ALTER TABLE vm_samples_history
  ADD CONSTRAINT vm_samples_history_current_user_id_fkey FOREIGN KEY (current_user_id)
      REFERENCES users_details_history (user_id) MATCH SIMPLE;

SELECT fn_db_add_column('vm_hourly_history', 'current_user_id', 'UUID');

ALTER TABLE vm_hourly_history
  ADD CONSTRAINT vm_hourly_history_current_user_id_fkey FOREIGN KEY (current_user_id)
      REFERENCES users_details_history (user_id) MATCH SIMPLE;

SELECT fn_db_add_column('vm_daily_history', 'current_user_id', 'UUID');

ALTER TABLE vm_daily_history
  ADD CONSTRAINT vm_daily_history_current_user_id_fkey FOREIGN KEY (current_user_id)
      REFERENCES users_details_history (user_id) MATCH SIMPLE;

SELECT fn_db_add_column('statistics_vms_users_usage_hourly', 'user_id', 'UUID');

ALTER TABLE statistics_vms_users_usage_hourly
  ADD CONSTRAINT statistics_vms_users_usage_hourly_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES users_details_history (user_id) MATCH SIMPLE;

SELECT fn_db_add_column('statistics_vms_users_usage_daily', 'user_id', 'UUID');

ALTER TABLE statistics_vms_users_usage_daily
  ADD CONSTRAINT statistics_vms_users_usage_daily_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES users_details_history (user_id) MATCH SIMPLE;
