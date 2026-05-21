/* Backorder count by channel */

SELECT	sales_channel,
		COUNT(*) AS backorder_count
FROM clean_orders
WHERE order_status = 'Backordered'
GROUP BY sales_channel
ORDER BY backorder_count DESC;