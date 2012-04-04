DELETE FROM enum_translator
 WHERE enum_type = 'REPORTS_PERIOD';

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 0, 'us-en', 'Daily'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 0
                              AND language_code = 'us-en'
                              AND value = 'Daily'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 1, 'us-en', 'Monthly'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 1
                              AND language_code = 'us-en'
                              AND value = 'Monthly'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 2, 'us-en', 'Quarterly'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 2
                              AND language_code = 'us-en'
                              AND value = 'Quarterly'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'REPORTS_PERIOD', 3, 'us-en', 'Yearly'
    WHERE  NOT EXISTS  (SELECT 1
                        FROM enum_translator
                        WHERE enum_type = 'REPORTS_PERIOD'
                              AND enum_key = 3
                              AND language_code = 'us-en'
                              AND value = 'Yearly'));
