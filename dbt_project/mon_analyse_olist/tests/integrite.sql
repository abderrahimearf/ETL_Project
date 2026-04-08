-- filepath: tests/assert_no_delivery_date_for_canceled_orders.sql
SELECT
    order_id,
    order_status,
    delivered_customer_at
FROM {{ ref('fact_orders') }}
WHERE order_status IN ('canceled', 'unavailable', 'processing')
  AND delivered_customer_at IS NOT NULL