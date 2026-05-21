/* Recommended reorder point by SKU */

WITH sales AS(
	SELECT	product_id,
			SUM(quantity) / NULLIF(COUNT(DISTINCT o.order_date), 0)::numeric AS avg_daily_demand
	FROM order_items oi
	JOIN clean_orders o ON oi.order_id = o.order_id
	GROUP BY product_id
),
	lead AS(
	SELECT	product_id,
			AVG(received_date - po_date) AS avg_lead_time
	FROM clean_purchase_orders
	WHERE received_date IS NOT NULL AND po_date IS NOT NULL
	GROUP BY product_id
)
SELECT	p.sku,
		p.product_name,
		COALESCE(s.avg_daily_demand, 0) AS avg_daily_demand,
		COALESCE(l.avg_lead_time, 0) AS avg_lead_time,
		CEIL(COALESCE(s.avg_daily_demand, 0) * COALESCE(l.avg_lead_time, 0) + 10) AS reorder_point
FROM clean_products p
LEFT JOIN sales s ON p.product_id = s.product_id
LEFT JOIN lead l ON p.product_id = l.product_id
ORDER BY reorder_point DESC;
		