/* Suppliers with long and variable lead times */

SELECT	s.supplier_name,
		AVG(po.received_date - po.po_date) AS avg_lead_time,
		STDDEV(po.received_date - po.po_date) AS lead_time_variability
FROM clean_purchase_orders po
JOIN suppliers s ON po.supplier_id = s.supplier_id
WHERE po.received_date IS NOT NULL AND po.po_date IS NOT NULL
GROUP BY s.supplier_name
ORDER BY lead_time_variability DESC NULLS LAST;