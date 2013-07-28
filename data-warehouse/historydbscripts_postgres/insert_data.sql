-- INSERT DATA to schema_version
INSERT INTO schema_version(version,script,checksum,installed_by,ended_at,state,current)
  values ('03010000','upgrade/03_01_0000_set_version.sql','0','engine',now(),'INSTALLED',true);
