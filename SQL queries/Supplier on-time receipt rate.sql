/* Supplier on-time receipt rate */

SELECT	s.supplier_name,
		COUNT(*) AS po_count,
		AVG(CASE
				WHEN po.received_date <= po.expected_date THEN 1.0
				ELSE 0.0 END) AS avg_on_time_rate
FROM clean_purchase_orders po
JOIN suppliers s ON po.supplier_id = s.supplier_id
WHERE po.received_date IS NOT NULL AND po.expected_date IS NOT NULL
GROUP BY s.supplier_name
ORDER BY avg_on_time_rate DESC;







