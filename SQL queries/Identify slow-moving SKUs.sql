/* Identify slow-moving SKUs */

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
		p.category,
		COALESCE(s.units_sold, 0) AS units_sold,
		COALESCE(i.units_on_hand, 0) AS units_on_hand
FROM clean_products p
LEFT JOIN sales s ON p.product_id = s.product_id
LEFT JOIN inv i ON p.product_id = i.product_id
WHERE COALESCE(s.units_sold, 0) < 10 AND COALESCE(i.units_on_hand, 0) > 0
ORDER BY units_on_hand DESC;





