/* monthly revenue trend */

SELECT	DATE_TRUNC('month', o.order_date) AS month,
		SUM(oi.unit_price * oi.quantity - oi.discount_amount) AS revenue
FROM clean_orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;