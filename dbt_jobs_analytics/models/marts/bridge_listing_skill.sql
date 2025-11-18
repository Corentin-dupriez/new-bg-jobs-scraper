with jobs as (
  select 
  {{dbt_utils.generate_surrogate_key(['listing_url', 'date_scraped'])}} as listing_id, 
  listing_url, 
  tech_stack
  from {{ ref('staging_jobs') }}
),

flattened as (
  select 
    listing_id,
    unnest(tech_stack) as skill_name
  from jobs
), 

skills as (
  select * 
  from {{ ref('dim_skills') }}
)

select 
  listing_id,
  s.skill_id
from flattened f
join skills s 
  on s.skill_name = f.skill_name
