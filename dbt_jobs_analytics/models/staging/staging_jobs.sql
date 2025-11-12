WITH jobs_cte AS (
  SELECT * 
  FROM {{source('main','jobs')}}
)

SELECT * 
FROM jobs_cte;
