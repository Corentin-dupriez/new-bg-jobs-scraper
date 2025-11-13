WITH company_info AS (
  select distinct(company_name) as company_name
  FROM {{ ref('staging_jobs') }}
)

select * 
from company_info
