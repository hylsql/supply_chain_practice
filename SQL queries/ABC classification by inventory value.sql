/* ABC classification by inventory value */

WITH sku_value AS(
	SELECT	p.sku,
			p.product_name,
			SUM(p.standard_cost * i.quantity_on_hand) AS inventory_value
	FROM clean_products p
	JOIN clean_inventory i ON p.product_id = i.product_id
	GROUP BY p.sku, p.product_name
),
	ranked AS(
	SELECT	*,
			SUM(inventory_value) OVER(ORDER BY inventory_value DESC)
							/ NULLIF(SUM(inventory_value) OVER(),0) AS cumulative_pct
	FROM sku_value
	)
SELECT	*,
		CASE
			WHEN cumulative_pct <= .80 THEN 'A'
			WHEN cumulative_pct <= .95 THEN 'B'
			ELSE 'C' END AS abc_class
FROM ranked
ORDER BY inventory_value DESC NULLS FIRST;