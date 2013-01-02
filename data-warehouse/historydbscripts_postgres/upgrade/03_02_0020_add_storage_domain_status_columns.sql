-- add storage_domain_status to statistics table
select fn_db_add_column('storage_domain_samples_history', 'storage_domain_status', 'smallint NOT NULL DEFAULT 1');
select fn_db_add_column('storage_domain_hourly_history', 'storage_domain_status', 'smallint NOT NULL DEFAULT 1');
select fn_db_add_column('storage_domain_daily_history', 'storage_domain_status', 'smallint NOT NULL DEFAULT 1');

-- add minutes in status to to statistics table
select fn_db_add_column('storage_domain_samples_history', 'minutes_in_status', 'DECIMAL(7,2) NOT NULL DEFAULT 1');
select fn_db_add_column('storage_domain_hourly_history', 'minutes_in_status', 'DECIMAL(7,2) NOT NULL DEFAULT 1');
select fn_db_add_column('storage_domain_daily_history', 'minutes_in_status', 'DECIMAL(7,2) NOT NULL DEFAULT 1');

-- add ENUMs to translator table
INSERT INTO enum_translator(enum_type,enum_key,language_code,value) SELECT 'STORAGE_DOMAIN_STATUS','0','us-en','Unattached' WHERE not exists (SELECT enum_type,enum_key,language_code,value FROM enum_translator WHERE enum_type = 'STORAGE_DOMAIN_STATUS' and enum_key =  '0' and language_code =  'us-en' and value =  'Unattached');
INSERT INTO enum_translator(enum_type,enum_key,language_code,value) SELECT 'STORAGE_DOMAIN_STATUS','1','us-en','Active' WHERE not exists (SELECT enum_type,enum_key,language_code,value FROM enum_translator WHERE enum_type = 'STORAGE_DOMAIN_STATUS' and enum_key =  '1' and language_code =  'us-en' and value =  'Active');
INSERT INTO enum_translator(enum_type,enum_key,language_code,value) SELECT 'STORAGE_DOMAIN_STATUS','2','us-en','InActive' WHERE not exists (SELECT enum_type,enum_key,language_code,value FROM enum_translator WHERE enum_type = 'STORAGE_DOMAIN_STATUS' and enum_key =  '2' and language_code =  'us-en' and value =  'Inactive');
INSERT INTO enum_translator(enum_type,enum_key,language_code,value) SELECT 'STORAGE_DOMAIN_STATUS','3','us-en','Mixed' WHERE not exists (SELECT enum_type,enum_key,language_code,value FROM enum_translator WHERE enum_type = 'STORAGE_DOMAIN_STATUS' and enum_key =  '3' and language_code =  'us-en' and value =  'Mixed');
INSERT INTO enum_translator(enum_type,enum_key,language_code,value) SELECT 'STORAGE_DOMAIN_STATUS','4','us-en','Locked' WHERE not exists (SELECT enum_type,enum_key,language_code,value FROM enum_translator WHERE enum_type = 'STORAGE_DOMAIN_STATUS' and enum_key =  '4' and language_code =  'us-en' and value =  'Locked');
