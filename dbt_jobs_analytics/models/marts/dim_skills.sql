with flattened as (
  select listing_url,
  unnest(tech_stack) as skill_name
  from {{ ref('staging_jobs') }}
)

select 
  {{ dbt_utils.generate_surrogate_key(['skill_name']) }} as skill_id,
  skill_name
from flattened
group by skill_name
