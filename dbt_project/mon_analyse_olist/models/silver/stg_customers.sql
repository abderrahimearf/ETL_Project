SELECT
    customer_id::TEXT,
    customer_unique_id::TEXT,
    NULLIF(customer_zip_code_prefix, '')::TEXT AS zip_code,
    UPPER(TRIM(NULLIF(customer_city, '')))::TEXT AS city,
    UPPER(NULLIF(customer_state, ''))::TEXT AS state_code
FROM {{ source('olist', 'customers') }}