{% macro calculate_order_total(price, quantity) %}
    ({{ price }} * {{ quantity }})
{% endmacro %}