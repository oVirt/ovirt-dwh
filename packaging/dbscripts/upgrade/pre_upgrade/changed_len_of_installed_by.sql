-- Changed length of installed by to true limit
ALTER TABLE schema_version ALTER COLUMN installed_by TYPE varchar(63);
