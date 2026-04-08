SELECT
    order_id::TEXT,
    NULLIF(payment_sequential, '')::INT AS payment_step,
    NULLIF(payment_type, '')::TEXT AS payment_type,
    NULLIF(payment_installments, '')::INT AS installments_count,
    NULLIF(payment_value, '')::DECIMAL(10,2) AS payment_amount
FROM {{ source('olist', 'order_payments') }}