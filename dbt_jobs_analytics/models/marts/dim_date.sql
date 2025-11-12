WITH date_spine as (
  {{ 
    dbt_utils.date_spine(
      datepart="day",
      start_date="cast('2023-01-01' as date)",
      end_date="cast('2026-12-31' as date)"
    ) 
  }}
)

select 
  cast(strftime('%Y%m%d', date_day) as int) as date_id,
  date_day,
  extract(day from date_day) as day,
  extract(month from date_day) as month,
  extract(year from date_day) as year,
  strftime('%W', date_day) as week,
  strftime('%A', date_day) as weekday,
  case 
    when strftime('%w', date_day) in ('0', '6') then true
    else false
  end as is_weekend
from date_spine
