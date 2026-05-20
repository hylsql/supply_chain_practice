/* Detect freight cost outliers */

/*	Threshold = AVG(Freight_cost) + 3 * STDDEV(Freight_cost) 
	Detect freight cost outliers	*/

SELECT *
FROM clean_shipments
WHERE freight_cost >(
	SELECT AVG(freight_cost) + 3 * STDDEV(freight_cost)
	FROM clean_shipments);







