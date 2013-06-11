--This file is a place holder for the creation of stored procedures in the oVirt Engine History database.
CREATE OR REPLACE FUNCTION update_enum_translator(enum_type varchar(40), enum_key smallint, language_code varchar(40), value text) RETURNS void AS $$
BEGIN
    DELETE FROM enum_translator
    WHERE enum_translator.enum_type = update_enum_translator.enum_type
          AND enum_translator.enum_key = update_enum_translator.enum_key
          AND enum_translator.language_code = update_enum_translator.language_code
          AND EXISTS (SELECT 1
                      FROM enum_translator as a
                      WHERE a.enum_type = update_enum_translator.enum_type
                            AND a.enum_key = update_enum_translator.enum_key
                            AND a.language_code = update_enum_translator.language_code);
    INSERT INTO enum_translator VALUES (update_enum_translator.enum_type, update_enum_translator.enum_key, update_enum_translator.language_code, update_enum_translator.value);
END;
$$ LANGUAGE plpgsql;
