SELECT
    product_id::TEXT,
    COALESCE(LOWER(NULLIF(product_category_name, '')), 'others')::TEXT AS category_name,
    NULLIF(product_weight_g, '')::INT AS weight_g,
    NULLIF(product_length_cm, '')::INT AS length_cm,
    NULLIF(product_height_cm, '')::INT AS height_cm,
    NULLIF(product_width_cm, '')::INT AS width_cm
FROM {{ source('olist', 'products') }}