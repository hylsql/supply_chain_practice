/* Build data quality status flags for products */

SELECT	product_id,
		sku,
		product_name,
		CASE
			WHEN sku IS NULL OR TRIM(sku) = '' THEN 'Missing SKU'
			WHEN standard_cost IS NULL OR standard_cost <= 0 THEN 'Invalid Cost'
			WHEN selling_price IS NULL OR selling_price <= 0 THEN 'Invalid Price'
			ELSE 'OK' END AS data_quality_status
FROM products;