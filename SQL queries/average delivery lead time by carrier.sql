/* Calculate average delivery lead time by carrier */

SELECT	carrier,
		AVG(delivered_date - shipped_date) AS avg_transit_days
FROM clean_shipments
WHERE delivered_date IS NOT NULL AND shipped_date IS NOT NULL
GROUP BY carrier
ORDER BY avg_transit_days DESC;







