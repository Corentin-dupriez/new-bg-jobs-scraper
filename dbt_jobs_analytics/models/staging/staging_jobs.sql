{% set columns = {
  "company_name": "company_name",
  'job_title': 'job_title',
  'location': 'location',
  'min_salary': "ifnull(replace(split(split(salary, ' лв.')[1], ' - ')[1], ' ', ''), 'Not communicated') as min_salary",
  "max_salary": "ifnull(replace(split(split(salary, ' лв.')[1], ' - ')[2], ' ', ''), 'Not communicated') as max_salary",
  "tech_stack": "tech_stack",
  "listing_url": "listing_url",
  "description": "description", 
  "date_posted": "date_posted",
  "categories": "categories",
  "company_activity": "ifnull(company_activity, 'Not communicated') as company_activity",
  "company_sector": "ifnull(company_sector, 'Not communicated') as company_sector",
  "company_central_office": "ifnull(company_central_office, 'Not communicated') as company_central_office",
  "company_creation_date": "ifnull(company_creation_date, 'Not communicated') as company_creation_date",
  "number_employees": "ifnull(number_employees, 'Not communicated') as number_employees",
  "implemented_in_bulgaria_date": "ifnull(implemented_in_bulgaria_date, 'Not communicated') as implemented_in_bulgaria_date",
  "number_employees_in_bulgaria": "ifnull(number_employees_in_bulgaria, 'Not communicated') as number_employees_in_bulgaria",
  "offices_in_bulgaria": "ifnull(offices_in_bulgaria, 'Not communicated') as offices_in_bulgaria",
  "it_employees_in_bulgaria": "ifnull(it_employees_in_bulgaria, 'Not communicated') as it_employees_in_bulgaria",
  "date_scraped": "date_scraped"
  } 
%}


WITH jobs_cte AS (
  SELECT 
  {% for c, query in columns.items() %}
    {{ query }} {% if not loop.last %},{% endif %}
  {% endfor %}
  FROM {{ source('main','jobs')}}
)

SELECT * 
FROM jobs_cte
