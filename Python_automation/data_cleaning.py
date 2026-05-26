import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

import smtplib
from email.message import EmailMessage

from datetime import datetime

# ==========================================
# LOAD .ENV FILE
# ==========================================

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

encoded_password = quote_plus(DB_PASSWORD)

connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}"
    f"/{DB_NAME}"
)

engine = create_engine(connection_string)

print("Connected to PostgreSQL.")

# ==========================================
# CREATE OUTPUT FOLDER
# ==========================================

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# HELPER FUNCTION
# ==========================================

def inspect_table(df, table_name):

    print(f"\n========== {table_name} ==========")

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

# ==========================================
# READ DATA FROM POSTGRESQL
# ==========================================

# ==========================================
# Customer Orders Table
# ==========================================

query = """
SELECT *
FROM customer_orders;
"""

customers_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    customers_df,
    "customer_orders"
)

# ==========================================
# Customer Orders Table CLEANING
# ==========================================

# Clean column names
customers_df.columns = (
    customers_df.columns
    .str.strip()
    .str.lower()
)

# order_date
customers_df["order_date"] = pd.to_datetime(
    customers_df["order_date"],
    errors="coerce"
)

# customer_region
customers_df["customer_region"] = (
    customers_df["customer_region"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# sales_channel
customers_df["sales_channel"] = (
    customers_df["sales_channel"]
    .astype(str)
    .str.strip()
    .str.title()
)

# order_status
customers_df["order_status"] = (
    customers_df["order_status"]
    .astype(str)
    .str.strip()
    .str.title()
)

# ==========================================
# REMOVE DUPLICATES
# ==========================================

customers_df = customers_df.drop_duplicates()

# ==========================================
# Export cleaned customer orders to CSV
# ==========================================


output_file = (
    OUTPUT_DIR
    / "cleaned_customer_orders.csv"
)

customers_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Cleaned file saved: {output_file}"
)

# ==========================================
# Inventory Table
# ==========================================

query = """
SELECT *
FROM inventory;
"""

inventory_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    inventory_df,
    "inventory"
)

# ==========================================
# Inventory Table CLEANING
# ==========================================

# Clean column names
inventory_df.columns = (
    inventory_df.columns
    .str.strip()
    .str.lower()
)

# Clean warehouse

inventory_df["warehouse"] = (
    inventory_df["warehouse"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

warehouse_mapping = {

    "SOUTH JORDAN": "South Jordan",

    "SLC": "Salt Lake City",

    "SALT LAKE CITY": "Salt Lake City",

    "DRPR": "Draper",

}

inventory_df["warehouse"] = (
    inventory_df["warehouse"]
    .replace(warehouse_mapping)
    .str.title()
)

# Clean quantity on hand

inventory_df["quantity_on_hand"] = (
    pd.to_numeric(
        inventory_df["quantity_on_hand"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

inventory_df = inventory_df[
    inventory_df["quantity_on_hand"] >= 0
]

# Clean last_updated

inventory_df["last_updated"] = pd.to_datetime(
    inventory_df["last_updated"],
    errors="coerce"
)

print(inventory_df.head(20))

# ==========================================
# Export cleaned inventory to CSV
# ==========================================


output_file = (
    OUTPUT_DIR
    / "cleaned_inventory.csv"
)

inventory_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Cleaned file saved: {output_file}"
)

# ==========================================
# order_items Table
# ==========================================

query = """
SELECT *
FROM order_items;
"""

order_items_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    order_items_df,
    "order_items"
)

# Clean column names
order_items_df.columns = (
    order_items_df.columns
    .str.strip()
    .str.lower()
)

# ==========================================
# Export cleaned order_items to CSV
# ==========================================

output_file = (
    OUTPUT_DIR
    / "cleaned_order_items.csv"
)

order_items_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Saved: {output_file}"
)

# ==========================================
# Products Table
# ==========================================

query = """
SELECT *
FROM products;
"""

products_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    products_df,
    "products"
)

# Clean column names

products_df.columns = (
    products_df.columns
    .str.strip()
    .str.lower()
)

# Clean sku

products_df["sku"] = (
    products_df["sku"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Clean product_name

products_df["product_name"] = (
    products_df["product_name"]
    .fillna("Unknown Product")
    .astype(str)
    .str.strip()
    .str.title()
)

# Clean category

products_df["category"] = (
    products_df["category"]
    .fillna("Unknown Category")
    .astype(str)
    .str.strip()
    .str.title()
)

# Clean standard_cost

products_df["standard_cost"] = (
    pd.to_numeric(
        products_df["standard_cost"],
        errors="coerce"
    )
)

products_df["standard_cost"] = (
    products_df.groupby("category")
    ["standard_cost"]
    .transform(
        lambda x: x.fillna(x.median())
    )
    .round(2)
)

# Clean selling price

products_df["selling_price"] = (
    pd.to_numeric(
        products_df["selling_price"],
        errors="coerce"
    )
    .fillna(0)
    .round(2)
)

# Clean supplier id

products_df["supplier_id"] = (
    pd.to_numeric(
        products_df["supplier_id"],
        errors="coerce"
    )
)

# Clean active flag

products_df["active_flag"] = (
    products_df["active_flag"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

active_mapping = {

    "Y": "Y",

    "YES": "Y",

    "N": "N",

    "NO": "N",

    "UNKNOWN": "Unknown"
}

products_df["active_flag"] = (
    products_df["active_flag"]
    .replace(active_mapping)
)

products_df = (
    products_df
    .drop_duplicates()
)

# ==========================================
# Export cleaned products to CSV
# ==========================================

output_file = (
    OUTPUT_DIR
    / "cleaned_products.csv"
)

products_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Saved: {output_file}"
)

# ==========================================
# Purchase Orders Table
# ==========================================

query = """
SELECT *
FROM purchase_orders;
"""

purchase_orders_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    purchase_orders_df,
    "purchase_orders"
)

# Clean column names
purchase_orders_df.columns = (
    purchase_orders_df.columns
    .str.strip()
    .str.lower()
)

inspect_table(
    purchase_orders_df,
    "purchase_orders"
)

# Clean column names

purchase_orders_df.columns = (
    purchase_orders_df.columns
    .str.strip()
    .str.lower()
)

# Clean warehouse

purchase_orders_df["warehouse"] = (
    purchase_orders_df["warehouse"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

warehouse_mapping = {

    "SOUTH JORDAN": "South Jordan",

    "SLC": "Salt Lake City",

    "SALT LAKE CITY": "Salt Lake City",

    "DRPR": "Draper",

}

purchase_orders_df["warehouse"] = (
    purchase_orders_df["warehouse"]
    .replace(warehouse_mapping)
    .str.title()
)

# Clean Date Columns

date_columns = [
    "po_date",
    "expected_date",
    "received_date"
]

for col in date_columns:

    purchase_orders_df[col] = (
        pd.to_datetime(
            purchase_orders_df[col],
            errors="coerce"
        )
    )

# Clean Ordered Quantity

purchase_orders_df["ordered_qty"] = (
    pd.to_numeric(
        purchase_orders_df["ordered_qty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

purchase_orders_df = purchase_orders_df[
    purchase_orders_df["ordered_qty"] >= 0
]

# Clean received quantity
purchase_orders_df["received_qty"] = (
    pd.to_numeric(
        purchase_orders_df["received_qty"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)

purchase_orders_df = purchase_orders_df[
    purchase_orders_df["received_qty"] >= 0
]

# Clean unit cost

purchase_orders_df["unit_cost"] = (
    pd.to_numeric(
        purchase_orders_df["unit_cost"],
        errors="coerce"
    )
    .fillna(0)
    .round(2)
)

purchase_orders_df = purchase_orders_df[
    purchase_orders_df["unit_cost"] >= 0
]

# Clean po_status

purchase_orders_df["po_status"] = (
    purchase_orders_df["po_status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Create PO lead time column

purchase_orders_df["lead_time_days"] = (
    purchase_orders_df["received_date"]
    -
    purchase_orders_df["po_date"]
).dt.days

# ==========================================
# Export cleaned purchase orders to CSV
# ==========================================

output_file = (
    OUTPUT_DIR
    / "cleaned_purchase_orders.csv"
)

purchase_orders_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Saved: {output_file}"
)

# ==========================================
# Shipments Table
# ==========================================

query = """
SELECT *
FROM shipments;
"""

shipments_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    shipments_df,
    "shipments"
)

# Clean column names

shipments_df.columns = (
    shipments_df.columns
    .str.strip()
    .str.lower()
)

# Clean ship_from_warehouse

shipments_df["ship_from_warehouse"] = (
    shipments_df["ship_from_warehouse"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

warehouse_mapping = {

    "DRAPER": "Draper",

    "DRPR": "Draper",

    "LEHI": "Lehi",

    "SOUTH JORDAN": "South Jordan",

    "SLC": "Salt Lake City",

    "SALT LAKE CITY": "Salt Lake City",

    "WEST VALLEY": "West Valley"
}

shipments_df["ship_from_warehouse"] = (
    shipments_df["ship_from_warehouse"]
    .replace(warehouse_mapping)
    .str.title()
)

# Convert Date Columns

date_columns = [

    "shipped_date",

    "promised_delivery_date",

    "delivered_date"
]

for col in date_columns:

    shipments_df[col] = (
        pd.to_datetime(
            shipments_df[col],
            errors="coerce"
        )
    )

# Clean freight_cost

shipments_df["freight_cost"] = (
    pd.to_numeric(
        shipments_df["freight_cost"],
        errors="coerce"
    )
    .fillna(0)
    .round(2)
)

shipments_df = shipments_df[
    shipments_df["freight_cost"] >= 0
]

# Clean shipment_status

shipments_df["shipment_status"] = (
    shipments_df["shipment_status"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Create Delivery delay days column

shipments_df["delivery_delay_days"] = (

    shipments_df["delivered_date"]

    -

    shipments_df["promised_delivery_date"]

).dt.days

# Create On-Time Flag

shipments_df["on_time_flag"] = (
    shipments_df["delivery_delay_days"] <= 0
)

on_time_rate = (
    shipments_df["on_time_flag"]
    .mean()
)

print(
    f"On-Time Delivery Rate: "
    f"{on_time_rate:.2%}"
)

# ==========================================
# Export cleaned shipments to CSV
# ==========================================

output_file = (
    OUTPUT_DIR
    / "cleaned_shipments.csv"
)

shipments_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Saved: {output_file}"
)

# ==========================================
# Clean Suppliers Table
# ==========================================

query = """
SELECT *
FROM suppliers;
"""

suppliers_df = pd.read_sql(
    query,
    engine
)

inspect_table(
    suppliers_df,
    "suppliers"
)

# Clean column names

suppliers_df.columns = (
    suppliers_df.columns
    .str.strip()
    .str.lower()
)

# Clean supplier_name
suppliers_df["supplier_name"] = (
    suppliers_df["supplier_name"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Clean supplier_country
suppliers_df["supplier_country"] = (
    suppliers_df["supplier_country"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

country_mapping = {
    "US": "United States",
    "CHINA": "China",
    "VIETNAM": "Vietnam",
    "MEXICO": "Mexico"
}

suppliers_df["supplier_country"] = (
    suppliers_df["supplier_country"]
    .replace(country_mapping)
)

# Clean payment_terms
suppliers_df["payment_terms"] = (
    suppliers_df["payment_terms"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.upper()
)

payment_terms_mapping = {
    "NET30": "Net 30",
    "NET 45": "Net 45",
    "NET 60": "Net 60",
    "UNKNOWN": "Unknown"
}

suppliers_df["payment_terms"] = (
    suppliers_df["payment_terms"]
    .replace(payment_terms_mapping)
)

# ==========================================
# Export cleaned suppliers to CSV
# ==========================================

output_file = OUTPUT_DIR / "cleaned_suppliers.csv"

suppliers_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"Saved: {output_file}")

inspect_table(
    suppliers_df,
    "suppliers"
)

# ==========================================
# CREATE BUSINESS DATASETS
# ==========================================

# 1. Sales dataset: orders + order items + products
sales_df = (
    customers_df
    .merge(order_items_df, on="order_id", how="left")
    .merge(products_df, on="product_id", how="left")
)

sales_df["revenue"] = (
    sales_df["quantity"] * sales_df["unit_price"]
) - sales_df["discount_amount"]

sales_df["total_cost"] = (
    sales_df["quantity"] * sales_df["standard_cost"]
)

sales_df["gross_profit"] = (
    sales_df["revenue"] - sales_df["total_cost"]
)

# 2. Inventory dataset: inventory + products
inventory_analysis_df = (
    inventory_df
    .merge(products_df, on="product_id", how="left")
)

inventory_analysis_df["inventory_value"] = (
    inventory_analysis_df["quantity_on_hand"]
    * inventory_analysis_df["standard_cost"]
)

# 3. Purchase order dataset: POs + suppliers + products
po_analysis_df = (
    purchase_orders_df
    .merge(suppliers_df, on="supplier_id", how="left")
    .merge(products_df, on="product_id", how="left")
)

po_analysis_df["lead_time_days"] = (
    po_analysis_df["received_date"] - po_analysis_df["po_date"]
).dt.days

po_analysis_df["fill_rate"] = (
    po_analysis_df["received_qty"] / po_analysis_df["ordered_qty"]
)

# 4. Shipment dataset: shipments + customer orders
shipment_analysis_df = (
    shipments_df
    .merge(customers_df, on="order_id", how="left")
)

shipment_analysis_df["delivery_delay_days"] = (
    shipment_analysis_df["delivered_date"]
    - shipment_analysis_df["promised_delivery_date"]
).dt.days

shipment_analysis_df["on_time_flag"] = (
    shipment_analysis_df["delivery_delay_days"] <= 0
)

print("Cleaned datasets exported successfully.")
