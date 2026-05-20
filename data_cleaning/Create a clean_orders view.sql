/* Create a clean_orders view */

CREATE OR REPLACE VIEW clean_orders AS
	SELECT	order_id,
			order_date,
			INITCAP(TRIM(customer_region)) AS customer_region,
			INITCAP(TRIM(sales_channel)) AS sales_channel,
			INITCAP(TRIM(order_status)) AS order_status
	FROM customer_orders;
SELECT *
FROM clean_orders;

