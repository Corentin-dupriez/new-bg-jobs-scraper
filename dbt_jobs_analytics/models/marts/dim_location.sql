WITH location as (
  SELECT distinct(location) as location_name
  from {{ ref('staging_jobs') }}
)

select location_name 
from location
