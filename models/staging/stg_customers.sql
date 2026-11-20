SELECT
    customer_id,
    TRIM(name) AS customer_name,
    TRIM(email) AS email

FROM customers