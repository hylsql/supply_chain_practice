/* Summarize product data quality counts */

WITH flags AS(
	SELECT	product_id,
		sku,
		product_name,
		CASE
			WHEN sku IS NULL OR TRIM(sku) = '' THEN 'Missing SKU'
			WHEN standard_cost IS NULL OR standard_cost <= 0 THEN 'Invalid Cost'
			WHEN selling_price IS NULL OR selling_price <= 0 THEN 'Invalid Price'
			ELSE 'OK' END AS data_quality_status
FROM products
)
SELECT	data_quality_status,
		COUNT(*)
FROM flags
GROUP BY data_quality_status
ORDER BY COUNT(*) DESC;
