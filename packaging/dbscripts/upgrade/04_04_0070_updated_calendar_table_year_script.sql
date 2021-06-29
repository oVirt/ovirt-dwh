-- Update calendar table year to 2051
TRUNCATE TABLE calendar;
INSERT INTO calendar( the_datetime, the_date, the_year, the_month, month_name, the_day, day_name, the_hour )
SELECT
     date_time as the_datetime,
     date_trunc('day', date_time) as the_date,
     extract (year from date_time) as the_year,
     extract (month from date_time) as the_month,
     initcap(to_char(date_time, 'FMmonth')) as month_name,
     extract (day from date_time) as the_day,
     initcap(to_char(date_time, 'FMday')) as day_name,
     cast(date_time as time) as the_hour
FROM
   (SELECT generate_series('2011-01-01 00:00'::timestamp, '2051-01-01 00:00', '1 hours') AS date_time) AS hour_list
ORDER BY date_time;