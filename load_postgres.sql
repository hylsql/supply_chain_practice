-- Update the path below to match your computer before running.
--

COPY suppliers FROM '/path/to/data/suppliers.csv' DELIMITER ',' CSV HEADER;
COPY products FROM '/path/to/data/products.csv' DELIMITER ',' CSV HEADER;
COPY inventory FROM '/path/to/data/inventory.csv' DELIMITER ',' CSV HEADER;
COPY customer_orders FROM '/path/to/data/customer_orders.csv' DELIMITER ',' CSV HEADER;
COPY order_items FROM '/path/to/data/order_items.csv' DELIMITER ',' CSV HEADER;
COPY shipments FROM '/path/to/data/shipments.csv' DELIMITER ',' CSV HEADER;
COPY purchase_orders FROM '/path/to/data/purchase_orders.csv' DELIMITER ',' CSV HEADER;
