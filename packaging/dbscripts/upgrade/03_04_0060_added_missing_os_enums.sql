--Update values of column operating_system according to OS Type where key equals to 6 to 1001
CREATE OR REPLACE FUNCTION __temp_update_operating_system() returns void
AS $function$
BEGIN
	UPDATE vm_configuration
	SET operating_system = 1001
	WHERE operating_system = 6;
END; $function$
LANGUAGE plpgsql;

SELECT __temp_update_operating_system();

DROP FUNCTION __temp_update_operating_system();

--Delete OS TYPEs from enum_translator table where enum_key equals to 6
CREATE OR REPLACE FUNCTION __temp_delete_from_enum_translator() returns void
AS $function$
BEGIN
	DELETE FROM enum_translator
	WHERE enum_type = 'OS_TYPE'
	AND enum_key = 6;
END; $function$
LANGUAGE plpgsql;

SELECT __temp_delete_from_enum_translator();

DROP FUNCTION __temp_delete_from_enum_translator();

--Updated value for enum_key 0
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('de' as varchar(40)),cast('Andere' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('en_US' as varchar(40)),cast('Other' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('es' as varchar(40)),cast('Otro' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('fr' as varchar(40)),cast('Autre' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('ja' as varchar(40)),cast('その他の' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('pt_BR' as varchar(40)),cast('Outro' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(0 as smallint),cast('zh_CN' as varchar(40)),cast('其他' as text));

--Updated value for enum_key 5
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('de' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('en_US' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('es' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('fr' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('ja' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('pt_BR' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(5 as smallint),cast('zh_CN' as varchar(40)),cast('Linux' as text));

--Updated value for enum_key 7
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(7 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 5.x' as text));


--Updated value for enum_key 8
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(8 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 4.x' as text));

--Updated value for enum_key 9
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(9 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 3.x' as text));

--Updated value for enum_key 13
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(13 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 5.x x64' as text));

--Updated value for enum_key 14
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(14 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 4.x x64' as text));

--Updated value for enum_key 15
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(15 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 3.x x64' as text));

--Updated value for enum_key 17
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('de' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('en_US' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('es' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('fr' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('ja' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('pt_BR' as varchar(40)),cast('Windows 2008 R2 x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(17 as smallint),cast('zh_CN' as varchar(40)),cast('Windows 2008 R2 x64' as text));

--Updated value for enum_key 18
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(18 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));

--Updated value for enum_key 19
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(19 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 6.x x64' as text));

--Added enum_key 1001
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('de' as varchar(40)),cast('Andere' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('en_US' as varchar(40)),cast('Other' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('es' as varchar(40)),cast('Otro' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('fr' as varchar(40)),cast('Autre' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('ja' as varchar(40)),cast('その他の' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('pt_BR' as varchar(40)),cast('Outro' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1001 as smallint),cast('zh_CN' as varchar(40)),cast('其他' as text));

--Add enum_key 1002
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('de' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('en_US' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('es' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('fr' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('ja' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('pt_BR' as varchar(40)),cast('Linux' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1002 as smallint),cast('zh_CN' as varchar(40)),cast('Linux' as text));

--Add enum_key 1003
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('de' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('en_US' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('es' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('fr' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('ja' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('pt_BR' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1003 as smallint),cast('zh_CN' as varchar(40)),cast('Red Hat Enterprise Linux 6.x' as text));

--Add enum_key 1004
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('de' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('en_US' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('es' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('fr' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('ja' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('pt_BR' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1004 as smallint),cast('zh_CN' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));

--Add enum_key 1193
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('de' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('en_US' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('es' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('fr' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('ja' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('pt_BR' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1193 as smallint),cast('zh_CN' as varchar(40)),cast('SUSE Linux Enterprise Server 11' as text));

--Add enum_key 1252
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('de' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('en_US' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('es' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('fr' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('ja' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('pt_BR' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1252 as smallint),cast('zh_CN' as varchar(40)),cast('Ubuntu Precise Pangolin LTS' as text));

--Add enum_key 1253
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('de' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('en_US' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('es' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('fr' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('ja' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('pt_BR' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1253 as smallint),cast('zh_CN' as varchar(40)),cast('Ubuntu Quantal Quetzal' as text));

--Add enum_key 1254
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('de' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('en_US' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('es' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('fr' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('ja' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('pt_BR' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1254 as smallint),cast('zh_CN' as varchar(40)),cast('Ubuntu Raring Ringtails' as text));

--Add enum_key 1255
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('de' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('en_US' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('es' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('fr' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('ja' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('pt_BR' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
SELECT update_enum_translator(cast('OS_TYPE' as varchar(40)),cast(1255 as smallint),cast('zh_CN' as varchar(40)),cast('Ubuntu Saucy Salamander' as text));
