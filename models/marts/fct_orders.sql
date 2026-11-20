SELECT
    o.order_id,
    o.status,
    o.order_date,
    o.notes,
    c.customer_id,
    c.customer_name,
    c.email

FROM {{ ref('stg_orders') }} o

LEFT JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id