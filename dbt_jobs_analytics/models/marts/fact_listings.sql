with dates as (
  select date_id, date_day 
  from dim_date
),jobs_cte as (
  select * 
  from {{ ref('staging_jobs') }}
), locations_cte as (
  select location_id,
  location_name 
  from {{ ref('dim_location') }}
)

select 
company_name, 
job_title, 
location,
min_salary,
max_salary,
tech_stack, 
listing_url, 
description,
dim_posted.date_id,
dim_scraped.date_id
from jobs_cte j
join dates as dim_posted on dim_posted.date_day = j.date_posted
join dates as dim_scraped on dim_scraped.date_day = j.date_scraped
left join locations_cte l on l.location_name = j.location
