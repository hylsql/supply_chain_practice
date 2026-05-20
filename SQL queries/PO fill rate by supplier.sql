/* PO fill rate by supplier */

SELECT	s.supplier_name,
		SUM(po.received_qty) AS received_qty,
		SUM(po.ordered_qty) AS ordered_qty,
		SUM(po.received_qty)::numeric
		/ NULLIF(SUM(po.ordered_qty), 0) AS po_fill_rate
FROM clean_purchase_orders po
JOIN suppliers s ON po.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY po_fill_rate DESC;







