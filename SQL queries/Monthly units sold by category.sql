/* Monthly units sold by category */

SELECT	DATE_TRUNC('month', o.order_date) AS month,
		p.category,
		SUM(oi.quantity) AS units_sold
FROM clean_orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN clean_products p ON oi.product_id = p.product_id
GROUP BY month, p.category
ORDER BY month, p.category;