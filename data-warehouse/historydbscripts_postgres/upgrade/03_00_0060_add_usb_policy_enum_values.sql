INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'USB_POLICY', 0, 'us-en', 'Enabled'
    WHERE  NOT EXISTS  (SELECT 1
			FROM 	enum_translator
			WHERE 	enum_type = 'USB_POLICY'
				AND enum_key = 0
				AND language_code = 'us-en'
				AND value = 'Enabled'));

INSERT INTO enum_translator(enum_type, enum_key, language_code, value)
    (SELECT 'USB_POLICY', 1, 'us-en', 'Disabled'
    WHERE  NOT EXISTS  (SELECT 1
			FROM 	enum_translator
			WHERE 	enum_type = 'USB_POLICY'
				AND enum_key = 1
				AND language_code = 'us-en'
				AND value = 'Disabled'));
