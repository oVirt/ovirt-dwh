/**************************************
    INTERNAL VIEWS FOR REPORTS
**************************************/

/*Views to create input controls for reports, since union is not possible in HQL currently*/

CREATE OR REPLACE VIEW rhev_reports_input_control_cluster
 AS
SELECT
      history_id as history_id,
      cluster_id as cluster_id,
            CASE
        WHEN delete_date IS NULL THEN cluster_name
        ELSE cluster_name || ' (Removed on ' || cast(delete_date as varchar) || ')'
      END as cluster_name_ic,
      datacenter_id as datacenter_id,
      delete_date as delete_date,
      0 as sort
FROM cluster_configuration
WHERE history_id in (SELECT max(a.history_id) FROM cluster_configuration as a GROUP BY a.cluster_id)
UNION ALL
SELECT -1, '11111111-1111-1111-1111-111111111111','All', '11111111-1111-1111-1111-111111111111', null, 1;

CREATE OR REPLACE VIEW rhev_reports_input_control_enum
 AS
SELECT  value,
    enum_key,
    enum_type,
    0 as sort
FROM v3_1_enum_translator_view
UNION ALL
SELECT 'All', -1, null, 1;
