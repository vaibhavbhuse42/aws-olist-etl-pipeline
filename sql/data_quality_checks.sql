USE olistdb;

-- Check missing customer IDs
SELECT COUNT(*) AS missing_customer_ids
FROM olist_customers
WHERE customer_id IS NULL OR customer_id = '';

-- Check missing order IDs
SELECT COUNT(*) AS missing_order_ids
FROM olist_orders
WHERE order_id IS NULL OR order_id = '';

-- Check negative item prices
SELECT COUNT(*) AS negative_item_prices
FROM olist_order_items
WHERE price < 0;

-- Check negative payment values
SELECT COUNT(*) AS negative_payment_values
FROM olist_order_payments
WHERE payment_value < 0;

-- Check duplicate customer IDs
SELECT customer_id, COUNT(*) AS occurrences
FROM olist_customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
