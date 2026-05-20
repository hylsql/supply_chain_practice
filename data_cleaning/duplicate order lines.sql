/* Find duplicate order lines by order and product */

SELECT	order_id,
		product_id,
		COUNT(*) AS line_count
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;