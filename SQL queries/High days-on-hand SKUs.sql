/* High days-on-hand SKUs */

WITH sales AS(
	SELECT	product_id,
			SUM(quantity) AS units_sold
	FROM order_items
	GROUP BY product_id
),
	inv AS(
	SELECT	product_id,
			SUM(quantity_on_hand) AS units_on_hand
	FROM clean_inventory
	GROUP BY product_id
)
SELECT	p.sku,
		p.product_name,
		COALESCE(s.units_sold, 0) AS units_sold,
		COALESCE(i.units_on_hand, 0) AS units_on_hand,
		COALESCE(s.units_sold, 0)::numeric / NULLIF(COALESCE(i.units_on_hand, 0), 0) AS inventory_turnover,
		365 / NULLIF(COALESCE(s.units_sold, 0)::numeric / NULLIF(COALESCE(i.units_on_hand, 0), 0), 0) AS days_on_hand
FROM clean_products p
JOIN inv i ON p.product_id = i.product_id
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE i.units_on_hand > 0
ORDER BY days_on_hand DESC NULLS LAST
LIMIT 25;