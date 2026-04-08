SELECT
    NULLIF(geolocation_zip_code_prefix, '')::TEXT AS zip_code,
    NULLIF(geolocation_lat, '')::DOUBLE PRECISION AS latitude,
    NULLIF(geolocation_lng, '')::DOUBLE PRECISION AS longitude,
    UPPER(TRIM(NULLIF(geolocation_city, '')))::TEXT AS city,
    UPPER(NULLIF(geolocation_state, ''))::TEXT AS state_code
FROM {{ source('olist', 'geolocation') }}