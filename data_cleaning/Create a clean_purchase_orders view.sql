/* Create a clean_purchase_orders view */

CREATE OR REPLACE VIEW clean_purchase_orders AS
	SELECT	po_id,
			supplier_id,
			product_id,
			CASE	WHEN LOWER(TRIM(warehouse)) IN ('draper','drpr') THEN ('Draper')
					WHEN LOWER(TRIM(warehouse)) IN ('salt lake city','slc') THEN ('Salt Lake City')
					ELSE INITCAP(TRIM(warehouse)) END AS warehouse,
			po_date,
			expected_date,
			received_date,
			ordered_qty,
			received_qty,
			unit_cost,
			INITCAP(TRIM(po_status)) AS po_status
	FROM purchase_orders;
SELECT *
FROM clean_purchase_orders;

