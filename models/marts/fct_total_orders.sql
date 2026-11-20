SELECT
    order_id,
    SUM(
        {{ calculate_order_total('unit_price', 'quantity') }}
    ) AS total_order_amount,
    SUM(quantity) AS total_quantity,
    COUNT(order_item_id) AS total_order_items
FROM {{ ref('stg_order_items') }}
GROUP BY order_id