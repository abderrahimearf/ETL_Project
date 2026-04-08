-- On cherche les commandes avec une date d'achat supérieure à "maintenant"
-- (Utile si ton pipeline tourne en temps réel ou avec des données simulées)
SELECT
    order_id,
    purchase_at
FROM {{ ref('stg_orders') }}
WHERE purchase_at > CURRENT_TIMESTAMP