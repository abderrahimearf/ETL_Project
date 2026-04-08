SELECT
    NULLIF(TRIM(_product_category_name::TEXT), '') AS category_name,
    NULLIF(TRIM(product_category_name_english::TEXT), '') AS category_name_english
FROM {{ source('olist', 'product_category_translation') }}