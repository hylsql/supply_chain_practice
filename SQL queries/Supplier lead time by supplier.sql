/* Supplier lead time by supplier */

SELECT	s.supplier_name,
		AVG(po.received_date - po.po_date) AS avg_lead_time
FROM clean_purchase_orders po
JOIN suppliers s ON po.supplier_id = s.supplier_id
WHERE po.received_date IS NOT NULL AND po.po_date IS NOT NULL
GROUP BY s.supplier_name
ORDER BY avg_lead_time DESC;







