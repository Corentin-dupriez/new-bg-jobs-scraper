with flattened as (
  select listing_url,
  unnest(categories) as category_name
  from {{ ref('staging_jobs') }}
)

select 
{{ dbt_utils.generate_surrogate_key(['category_name']) }} as category_id,
category_name
from flattened
group by category_name, category_id
