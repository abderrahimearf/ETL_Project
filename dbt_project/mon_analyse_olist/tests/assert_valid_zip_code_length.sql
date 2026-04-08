-- On cherche les clients dont le code postal est trop court ou aberrant
SELECT
    customer_id,
    zip_code,
    LENGTH(zip_code::TEXT) as zip_len
FROM {{ ref('stg_customers') }}
WHERE LENGTH(zip_code::TEXT) < 5 
   OR LENGTH(zip_code::TEXT) > 8