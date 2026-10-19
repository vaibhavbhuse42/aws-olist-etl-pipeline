USE olistdb;

SHOW TABLES;

SELECT 'customers' AS dataset, COUNT(*) AS total_rows
FROM olist_customers

UNION ALL

SELECT 'orders', COUNT(*)
FROM olist_orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM olist_order_items

UNION ALL

SELECT 'order_payments', COUNT(*)
FROM olist_order_payments

UNION ALL

SELECT 'products', COUNT(*)
FROM olist_products;
