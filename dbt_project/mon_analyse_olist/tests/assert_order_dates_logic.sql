-- On cherche les commandes où la date de livraison est antérieure à la date d'achat
SELECT
    order_id,
    purchase_at,
    delivered_customer_at
FROM {{ ref('stg_orders') }}
WHERE delivered_customer_at < purchase_at
  AND delivered_customer_at IS NOT NULL