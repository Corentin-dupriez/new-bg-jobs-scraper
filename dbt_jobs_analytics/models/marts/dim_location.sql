WITH location as (
  SELECT distinct(location) as location_name
  from {{ ref('staging_jobs') }}
)

select 
{{ dbt_utils.generate_surrogate_key(['location_name'])}} as location_id,
location_name 
from location
