WITH payment_totals AS (
    SELECT
        order_id,
        SUM(payment_amount) AS total_paid,
        MAX(installments_count) AS max_installments
    FROM {{ ref('stg_order_payments') }}
    GROUP BY order_id
),
item_totals AS (
    SELECT
        order_id,
        SUM(price) AS total_items_price,
        SUM(freight_value) AS total_freight,
        COUNT(item_number) AS total_items_count
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_at,
    o.delivered_customer_at,
    -- Extraction en entier pour faciliter le calcul de moyenne (AVG)
    EXTRACT(DAY FROM (o.delivered_customer_at - o.purchase_at))::INT AS delivery_time_days,
    o.is_late,
    p.total_paid,
    p.max_installments,
    i.total_items_price,
    i.total_freight,
    i.total_items_count
FROM {{ ref('stg_orders') }} o
LEFT JOIN payment_totals p ON o.order_id = p.order_id
LEFT JOIN item_totals i ON o.order_id = i.order_id