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
), company_cte as (
  select company_id,
  company_name
  from {{ ref('dim_company') }}
)

select 
  {{ dbt_utils.generate_surrogate_key(['j.listing_url', 'j.date_scraped']) }} as listing_id,
  c.company_id,
  job_title, 
  location_id,
  min_salary,
  max_salary,
  listing_url,
  description,
  dim_posted.date_id as date_posted_id,
  dim_scraped.date_id as date_scraped_id
from jobs_cte j
join dates as dim_posted on dim_posted.date_day = j.date_posted
join dates as dim_scraped on dim_scraped.date_day = j.date_scraped
left join locations_cte l on l.location_name = j.location
join company_cte c on c.company_name = j.company_name
