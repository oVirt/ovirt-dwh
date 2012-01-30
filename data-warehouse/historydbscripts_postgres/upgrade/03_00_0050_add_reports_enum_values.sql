INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_SHOW_DELETED', 0, 'us-en', 'No'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_SHOW_DELETED'
                              AND enum_key = 0
                              AND language_code = 'us-en'
                              AND value = 'No'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_SHOW_DELETED', 1, 'us-en', 'Yes'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_SHOW_DELETED'
                              AND enum_key = 1
                              AND language_code = 'us-en'
                              AND value = 'Yes'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 0, 'us-en', 'Monthly'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 0
                              AND language_code = 'us-en'
                              AND value = 'Monthly'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 1, 'us-en', 'Quarterly'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 1
                              AND language_code = 'us-en'
                              AND value = 'Quarterly'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_ALL', 0, 'us-en', 'All'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_ALL'
                              AND enum_key = 0
                              AND language_code = 'us-en'
                              AND value = 'All'));

DROP TABLE period;
