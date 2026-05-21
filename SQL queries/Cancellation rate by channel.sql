/* Cancellation rate by channel */

SELECT	sales_channel,
		COUNT(*) AS orders,
		AVG(CASE
				WHEN order_status = 'Cancelled' THEN 1.0
				ELSE 0.0 END) AS cancellation_rate
FROM clean_orders
GROUP BY sales_channel
ORDER BY cancellation_rate DESC;