-- filepath: tests/assert_order_financial_consistency.sql

WITH payment_sums AS (
    SELECT 
        order_id, 
        SUM(payment_amount) AS total_paid
    FROM {{ ref('stg_order_payments') }}
    GROUP BY 1
),
item_sums AS (
    SELECT 
        order_id, 
        SUM(price + freight_value) AS total_order_value
    FROM {{ ref('stg_order_items') }}
    GROUP BY 1
)

SELECT 
    p.order_id,
    p.total_paid,
    i.total_order_value,
    ABS(p.total_paid - i.total_order_value) AS delta
FROM payment_sums p
JOIN item_sums i ON p.order_id = i.order_id
-- On filtre pour ne voir que les erreurs (différence > 0.01 pour l'arrondi)
WHERE ABS(p.total_paid - i.total_order_value) > 0.01