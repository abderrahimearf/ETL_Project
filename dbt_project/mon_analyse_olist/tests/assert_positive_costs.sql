-- On cherche les articles avec des prix aberrants (<= 0)
SELECT
    order_id,
    product_id,
    price,
    freight_value
FROM {{ ref('stg_order_items') }}
WHERE price <= 0 OR freight_value < 0