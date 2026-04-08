SELECT
    customer_id,
    customer_unique_id,
    zip_code,
    city,
    state_code
FROM {{ ref('stg_customers') }}



