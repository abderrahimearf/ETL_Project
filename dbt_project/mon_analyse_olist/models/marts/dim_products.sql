SELECT
    p.product_id,
    p.weight_g,
    p.length_cm,
    p.height_cm,
    p.width_cm,
    COALESCE(t.category_name_english, p.category_name)::TEXT AS category_name
FROM {{ ref('stg_products') }} p
LEFT JOIN {{ ref('stg_category_translation') }} t
    ON p.category_name = t.category_name