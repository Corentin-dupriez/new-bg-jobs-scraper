WITH location as (
  SELECT distinct(location)
  from {{ ref('staging_jobs') }}
)

select * 
from location
