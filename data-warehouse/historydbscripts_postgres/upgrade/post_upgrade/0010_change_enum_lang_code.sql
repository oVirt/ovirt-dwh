UPDATE enum_translator
SET language_code = 'en_US'
WHERE language_code = 'us-en';

UPDATE enum_translator
SET language_code = 'zh_CN'
WHERE language_code = 'zh-CN';

UPDATE enum_translator
SET language_code = '"pt_BR"'
WHERE language_code = 'pt-BR';
