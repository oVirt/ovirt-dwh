INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_NONE_AVAILABLE', 0, 'en_US', 'None Available'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_NONE_AVAILABLE'
                              AND enum_key = 0
                              AND language_code = 'en_US'
                              AND value = 'None Available'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_REMOVED_ON', 0, 'en_US', 'Removed on'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_REMOVED_ON'
                              AND enum_key = 0
                              AND language_code = 'en_US'
                              AND value = 'Removed on'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_DETACHED_ON', 0, 'en_US', 'Detached on'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_DETACHED_ON'
                              AND enum_key = 0
                              AND language_code = 'en_US'
                              AND value = 'Detached on'));
