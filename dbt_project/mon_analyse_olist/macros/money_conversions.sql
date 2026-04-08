-- macros/money_conversions.sql

{% macro cents_to_euro(column_name) %}
    round(({{ column_name }} / 100)::numeric, 2)
{% endmacro %}