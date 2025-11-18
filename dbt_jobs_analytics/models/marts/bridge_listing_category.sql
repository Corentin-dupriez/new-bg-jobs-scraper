with jobs as (
  select 
  {{ dbt_utils.generate_surrogate_key(['listing_url', 'date_scraped'])}} as listing_id,
  listing_url,
  categories
  from {{ ref('staging_jobs') }}
), 
flattened as (
  select 
  listing_id,
  unnest(categories) as category_name
  from jobs
),
categories as (
  select 
  category_id,
  category_name
  from {{ ref('dim_categories') }}
)

select listing_id,
c.category_id
from flattened f
join categories c
on c.category_name = f.category_name
