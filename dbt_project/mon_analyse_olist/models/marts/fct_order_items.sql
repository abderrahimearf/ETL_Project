SELECT
    oi.order_id,
    oi.item_number,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_at,
    oi.price,
    oi.freight_value,
    oi.total_item_value,
    o.customer_id,
    o.order_status,
    o.purchase_at,
    o.delivered_customer_at,
    o.is_late
FROM {{ ref('stg_order_items') }} oi
INNER JOIN {{ ref('stg_orders') }} o 
    ON oi.order_id = o.order_id