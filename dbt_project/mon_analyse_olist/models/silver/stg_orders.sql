SELECT
    order_id::TEXT AS order_id,
    customer_id::TEXT AS customer_id,

    UPPER(TRIM(order_status::TEXT)) AS order_status,

    NULLIF(TRIM(order_purchase_timestamp::TEXT), '')::TIMESTAMP AS purchase_at,
    NULLIF(TRIM(order_approved_at::TEXT), '')::TIMESTAMP AS approved_at,
    NULLIF(TRIM(order_delivered_carrier_date::TEXT), '')::TIMESTAMP AS delivered_carrier_at,
    NULLIF(TRIM(order_delivered_customer_date::TEXT), '')::TIMESTAMP AS delivered_customer_at,
    NULLIF(TRIM(order_estimated_delivery_date::TEXT), '')::TIMESTAMP AS estimated_delivery_at,

    EXTRACT(
        DAY FROM (
            NULLIF(TRIM(order_delivered_customer_date::TEXT), '')::TIMESTAMP
            - NULLIF(TRIM(order_purchase_timestamp::TEXT), '')::TIMESTAMP
        )
    )::INT AS delivery_time_days,

    CASE
        WHEN NULLIF(TRIM(order_delivered_customer_date::TEXT), '')::TIMESTAMP
             > NULLIF(TRIM(order_estimated_delivery_date::TEXT), '')::TIMESTAMP
        THEN 1
        ELSE 0
    END AS is_late

FROM {{ source('olist', 'orders') }}