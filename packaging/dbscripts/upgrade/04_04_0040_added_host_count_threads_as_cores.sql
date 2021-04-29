-- Added cluster count threads as cores
select fn_db_add_column('cluster_configuration', 'count_threads_as_cores', 'boolean');