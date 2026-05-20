/* Create a clean_shipments view */

CREATE OR REPLACE VIEW clean_shipments AS
	SELECT	shipment_id,
			order_id,
			UPPER(TRIM(carrier)) AS carrier,
			CASE	WHEN LOWER(TRIM(ship_from_warehouse)) IN ('draper','drpr') THEN ('Draper')
					WHEN LOWER(TRIM(ship_from_warehouse)) IN ('salt lake city','slc') THEN ('Salt Lake City')
					ELSE INITCAP(TRIM(ship_from_warehouse)) END AS ship_from_warehouse,
			shipped_date,
			promised_delivery_date,
			delivered_date,
			freight_cost,
			INITCAP(TRIM(shipment_status)) AS shipment_status
	FROM shipments;
SELECT *
FROM clean_shipments;
