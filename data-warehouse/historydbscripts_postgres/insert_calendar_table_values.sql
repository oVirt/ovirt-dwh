INSERT INTO calendar(the_datetime, the_date, the_year, the_month, month_name, the_day, day_name, the_hour)
SELECT
     b.h as the_datetime,
     d.dates as the_date,
     extract (year from d.dates) as the_year,
     extract (month from d.dates) as the_month,
     initcap(to_char(d.dates, 'FMmonth')) as month_name,
     extract (day from d.dates) as the_day,
     initcap(to_char(d.dates, 'FMday')) as day_name,
     cast(b.h as time) as the_hour
FROM
   (select (to_date('29/03/2011', 'DD/MM/YYYY') + s.a) as dates
    from generate_series(0, 4000) as s(a)) d,
   (SELECT (TIMESTAMP 'epoch' + h * INTERVAL '1 second') AS h
    FROM  (SELECT generate_series(EXTRACT(EPOCH FROM DATE_TRUNC('hour', to_timestamp('29/03/2011', 'DD/MM/YYYY')))::bigint,
      (EXTRACT(EPOCH FROM to_timestamp('29/03/2020', 'DD/MM/YYYY'))::bigint), 60*60) as h) as hour_lists) as b
WHERE d.dates = cast(b.h as date)
ORDER BY b.h;
