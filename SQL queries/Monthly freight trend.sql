/* Monthly freight trend */

SELECT	DATE_TRUNC('month', s.shipped_date) AS month,
		SUM(s.freight_cost) AS freight_cost
FROM clean_shipments s
GROUP BY DATE_TRUNC('month', s.shipped_date)
ORDER BY month;