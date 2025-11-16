WITH company_info AS (
  select 
  company_name,
  company_activity,
  company_sector,
  company_central_office,
  company_creation_date,
  number_employees,
  implemented_in_bulgaria_date,
  number_employees_in_bulgaria,
  offices_in_bulgaria,
  it_employees_in_bulgaria
  FROM {{ ref('staging_jobs')}}
  group by 
  company_name,
  company_activity,
  company_sector,
  company_central_office,
  company_creation_date,
  number_employees,
  implemented_in_bulgaria_date,
  number_employees_in_bulgaria,
  offices_in_bulgaria,
  it_employees_in_bulgaria
)

select 
{{dbt_utils.generate_surrogate_key(['company_name'])}} as company_id,
company_name,
company_activity,
company_sector,
company_central_office,
company_creation_date,
number_employees,
implemented_in_bulgaria_date,
number_employees_in_bulgaria,
offices_in_bulgaria,
it_employees_in_bulgaria
from company_info
