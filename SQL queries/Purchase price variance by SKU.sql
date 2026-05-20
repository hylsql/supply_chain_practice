/* Purchase price variance by SKU */

SELECT	p.sku,
		p.product_name,
		AVG(po.unit_cost) AS avg_po_cost,
		AVG(p.standard_cost) AS avg_standard_cost,
		AVG(po.unit_cost) - AVG(p.standard_cost) AS purchase_price_variance
FROM clean_products p
JOIN clean_purchase_orders po ON p.product_id = po.product_id
GROUP BY p.sku, p.product_name, p.standard_cost
ORDER BY ABS(AVG(po.unit_cost)) DESC NULLS FIRST;








