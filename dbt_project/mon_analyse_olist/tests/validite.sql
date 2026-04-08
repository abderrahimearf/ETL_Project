-- filepath: tests/assert_estimated_date_is_logical.sql
SELECT
    order_id,
    purchase_at,
    estimated_delivery_at
FROM {{ ref('fact_orders') }}
WHERE estimated_delivery_at < purchase_at