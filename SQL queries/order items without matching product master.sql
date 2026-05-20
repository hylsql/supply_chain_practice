/* Find order items without matching product master */

SELECT	oi.*
FROM order_items oi LEFT JOIN products p ON oi.product_id=p.product_id
WHERE p.product_id IS NULL;