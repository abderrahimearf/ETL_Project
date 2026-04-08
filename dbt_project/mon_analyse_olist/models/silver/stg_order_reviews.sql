SELECT
    review_id::TEXT AS review_id,
    order_id::TEXT AS order_id,

    NULLIF(TRIM(review_score::TEXT), '')::INT AS score,
    NULLIF(TRIM(review_comment_title::TEXT), '') AS review_comment_title,
    NULLIF(TRIM(review_comment_message::TEXT), '') AS review_comment_message,

    NULLIF(TRIM(review_creation_date::TEXT), '')::TIMESTAMP AS created_at,
    NULLIF(TRIM(review_answer_timestamp::TEXT), '')::TIMESTAMP AS answered_at

FROM {{ source('olist', 'order_reviews') }}