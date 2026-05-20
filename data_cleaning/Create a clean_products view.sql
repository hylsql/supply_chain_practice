/* Create a clean_products view */

CREATE OR REPLACE VIEW clean_inventory AS 
	SELECT	product_id,
			UPPER(REPLACE(TRIM(sku), ' ', '')) AS sku,
			INITCAP(TRIM(product_name)) AS product_name,
			INITCAP(TRIM(category)) AS category,
			Standard_cost,
			Selling_price,
			Supplier_id,
			CASE	WHEN LOWER(TRIM(active_flag)) IN ('y','yes') THEN 'Y'
					WHEN LOWER(TRIM(active_flag)) IN ('n','no') THEN 'N'
					ELSE 'Unknown' END AS active_flag
	FROM products;
