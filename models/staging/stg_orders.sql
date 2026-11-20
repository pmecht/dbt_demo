SELECT
    order_id,
    customer_id,
    order_date,
    notes,
    status

FROM orders
WHERE status = 'delivered'