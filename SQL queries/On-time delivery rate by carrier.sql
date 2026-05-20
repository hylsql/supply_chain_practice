/*  On-time delivery rate by carrier */

SELECT	carrier,
		COUNT(*) AS shipments,
		AVG(CASE
			WHEN delivered_date <= promised_delivery_date THEN 1.0
			ELSE 0.0 END) AS on_time_delivery_rate
FROM clean_shipments
WHERE delivered_date IS NOT NULL AND promised_delivery_date IS NOT NULL
GROUP BY carrier
ORDER BY on_time_delivery_rate DESC;








