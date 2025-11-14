with jobs as (
  select listing_id, 
  listing_url, 
  tech_stack
  from {{ ref('fact_listings') }}
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
