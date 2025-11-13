{% set columns = {
  "company_name": "company_name",
  'job_title': 'job_title',
  'location': 'location',
  'min_salary': "ifnull(split(split(salary, ' лв.')[1], ' - ')[1], 'Not communicated') as min_salary",
  "max_salary": "ifnull(split(split(salary, ' лв.')[1], ' - ')[2], 'Not communicated') as max_salary",
  "tech_stack": "tech_stack",
  "listing_url": "listing_url",
  "description": "description", 
  "date_posted": "date_posted",
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
