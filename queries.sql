-- 1. Monthly completed revenue
SELECT substr(o.order_date,1,7) AS month, ROUND(SUM(oi.quantity*oi.unit_price),2) AS revenue
FROM orders o JOIN order_items oi ON o.order_id=oi.order_id WHERE o.status='Completed' GROUP BY month ORDER BY month;

-- 2. Top customers by completed revenue
SELECT c.customer_id,c.customer_name,ROUND(SUM(oi.quantity*oi.unit_price),2) AS lifetime_value
FROM customers c JOIN orders o ON c.customer_id=o.customer_id JOIN order_items oi ON o.order_id=oi.order_id
WHERE o.status='Completed' GROUP BY c.customer_id,c.customer_name ORDER BY lifetime_value DESC LIMIT 20;

-- 3. Category performance
SELECT p.category, ROUND(SUM(oi.quantity*oi.unit_price),2) AS revenue, SUM(oi.quantity) AS units
FROM products p JOIN order_items oi ON p.product_id=oi.product_id JOIN orders o ON oi.order_id=o.order_id
WHERE o.status='Completed' GROUP BY p.category ORDER BY revenue DESC;
