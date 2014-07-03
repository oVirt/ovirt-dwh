-- Changed external_id type to text to allow match engine
ALTER TABLE users_details_history ALTER COLUMN external_id DROP DEFAULT;
SELECT fn_db_change_column_type('users_details_history', 'external_id', 'bytea', 'text');
ALTER TABLE users_details_history ALTER COLUMN external_id SET NOT NULL;
