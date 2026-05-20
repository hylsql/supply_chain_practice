/* Freight percentage of revenue by order */

WITH rev AS(
	SELECT	order_id,
			SUM(unit_price * quantity - discount_amount) AS revenue
	FROM order_items
	GROUP BY order_id
),
	fr AS(
	SELECT	order_id,
			SUM(freight_cost) AS freight_cost
	FROM shipments
	GROUP BY order_id
)
SELECT	r.order_id,
		r.revenue,
		COALESCE(f.freight_cost, 0) AS freight_cost,
		COALESCE(f.freight_cost, 0)
		/ NULLIF(r.revenue, 0) AS freight_pct
FROM rev r
LEFT JOIN fr f ON r.order_id = f.order_id
ORDER BY freight_pct DESC;







