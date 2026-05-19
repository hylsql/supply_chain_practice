-- Supply Chain SQL Practice Schema (PostgreSQL)
DROP TABLE IF EXISTS order_items, shipments, customer_orders, inventory, purchase_orders, products, suppliers CASCADE;
CREATE TABLE suppliers (supplier_id INT PRIMARY KEY, supplier_name TEXT, supplier_country TEXT, payment_terms TEXT);
CREATE TABLE products (product_id INT PRIMARY KEY, sku TEXT, product_name TEXT, category TEXT, standard_cost NUMERIC, selling_price NUMERIC, supplier_id INT, active_flag TEXT);
CREATE TABLE inventory (inventory_id INT PRIMARY KEY, product_id INT, warehouse TEXT, quantity_on_hand INT, last_updated DATE);
CREATE TABLE customer_orders (order_id INT PRIMARY KEY, order_date DATE, customer_region TEXT, sales_channel TEXT, order_status TEXT);
CREATE TABLE order_items (order_item_id INT PRIMARY KEY, order_id INT, product_id INT, quantity INT, unit_price NUMERIC, discount_amount NUMERIC);
CREATE TABLE shipments (shipment_id INT PRIMARY KEY, order_id INT, carrier TEXT, ship_from_warehouse TEXT, shipped_date DATE, promised_delivery_date DATE, delivered_date DATE, freight_cost NUMERIC, shipment_status TEXT);
CREATE TABLE purchase_orders (po_id INT PRIMARY KEY, supplier_id INT, product_id INT, warehouse TEXT, po_date DATE, expected_date DATE, received_date DATE, ordered_qty INT, received_qty INT, unit_cost NUMERIC, po_status TEXT);
