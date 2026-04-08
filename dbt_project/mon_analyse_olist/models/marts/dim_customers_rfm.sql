-- Exemple de logique RFM simplifiée dans dbt
WITH customer_orders AS (
    SELECT 
        customer_unique_id,
        MAX(purchase_at) as last_purchase,
        COUNT(order_id) as frequency,
        SUM(total_paid) as monetary
    FROM {{ ref('fct_orders') }}
    JOIN {{ ref('dim_customers') }} USING (customer_id)
    GROUP BY 1
)
SELECT 
    customer_unique_id,
    DATE_PART('day', CURRENT_DATE - last_purchase) as recency,
    frequency,
    monetary
FROM customer_orders