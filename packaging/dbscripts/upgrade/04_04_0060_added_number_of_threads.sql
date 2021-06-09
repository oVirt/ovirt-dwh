-- Added host number of threads
SELECT fn_db_add_column('host_configuration', 'number_of_threads', 'smallint');

-- Copy threads_per_core values to number_of_threads
UPDATE host_configuration SET number_of_threads = threads_per_core;