/* Create a clean_inventory view */

CREATE OR REPLACE VIEW clean_inventory AS 
	SELECT	inventory_id,
			product_id,
			CASE	WHEN LOWER(TRIM(warehouse)) IN ('south jordan','SOUTH JORDAN') THEN 'South Jordan'
					WHEN LOWER(TRIM(warehouse)) IN ('Draper','DRPR') THEN 'Draper'
					WHEN LOWER(TRIM(warehouse)) IN ('Salt Lake City','SLC') THEN 'Salt Lake City'
					ELSE INITCAP(TRIM(warehouse)) END AS warehouse,
			CASE	WHEN quantity_on_hand < 0 THEN 0
					ELSE quantity_on_hand END AS quantity_on_hand,
			last_updated
	FROM inventory;
SELECT *
FROM clean_inventory;
