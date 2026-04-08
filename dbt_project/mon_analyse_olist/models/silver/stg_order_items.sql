SELECT
    order_id::TEXT AS order_id,

    NULLIF(TRIM(order_item_id::TEXT), '')::INT AS item_number,
    product_id::TEXT AS product_id,
    seller_id::TEXT AS seller_id,

    NULLIF(TRIM(shipping_limit_date::TEXT), '')::TIMESTAMP AS shipping_limit_at,

    NULLIF(TRIM(price::TEXT), '')::DECIMAL(10,2) AS price,
    NULLIF(TRIM(freight_value::TEXT), '')::DECIMAL(10,2) AS freight_value,

    COALESCE(NULLIF(TRIM(price::TEXT), '')::DECIMAL(10,2), 0)
    + COALESCE(NULLIF(TRIM(freight_value::TEXT), '')::DECIMAL(10,2), 0)
    AS total_item_value

FROM {{ source('olist', 'order_items') }}