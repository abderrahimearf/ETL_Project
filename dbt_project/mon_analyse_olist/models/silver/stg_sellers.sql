SELECT
    seller_id::TEXT,
    NULLIF(seller_zip_code_prefix, '')::TEXT AS zip_code,
    UPPER(TRIM(NULLIF(seller_city, '')))::TEXT AS city,
    UPPER(NULLIF(seller_state, ''))::TEXT AS state_code
FROM {{ source('olist', 'sellers') }}