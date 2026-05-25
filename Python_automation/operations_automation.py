from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

inventory_df = pd.read_csv(OUTPUT_DIR / "inventory_dataset.csv")
sales_df = pd.read_csv(OUTPUT_DIR / "sales_dataset.csv")
po_df = pd.read_csv(OUTPUT_DIR / "purchase_order_dataset.csv")

# Convert date columns to datetime

sales_df["order_date"] = pd.to_datetime(
    sales_df["order_date"],
    errors="coerce"
)

# Calculate Number of Sales Days

total_days = (
    sales_df["order_date"].max()
    -
    sales_df["order_date"].min()
).days

if total_days == 0:
    total_days = 1

print(total_days)

# Calculate Units Sold Per Product

product_sales_df = (
    sales_df

    .groupby("product_id", as_index=False)

    .agg(
        total_units_sold=("quantity", "sum")
    )
)

# Create Average Daily Sales

product_sales_df["avg_daily_sales"] = (
    product_sales_df["total_units_sold"]
    / total_days
)

# Calculate Average Lead Time Per Product

lead_time_df = (

    po_df

    .groupby("product_id", as_index=False)

    .agg(
        avg_lead_time_days=(
            "lead_time_days",
            "mean"
        )
    )
)

# Merge Into Inventory Dataset

inventory_alerts_df = (

    inventory_df

    .merge(
        product_sales_df[
            [
                "product_id",
                "avg_daily_sales"
            ]
        ],
        on="product_id",
        how="left"
    )

    .merge(
        lead_time_df,
        on="product_id",
        how="left"
    )
)

# Fill Missing Values

inventory_alerts_df["avg_daily_sales"] = (
    inventory_alerts_df["avg_daily_sales"]
    .fillna(0)
)

inventory_alerts_df["avg_lead_time_days"] = (
    inventory_alerts_df["avg_lead_time_days"]
    .fillna(0)
)

# Create Reorder Point

inventory_alerts_df["reorder_point"] = (

    inventory_alerts_df["avg_daily_sales"]

    *

    inventory_alerts_df["avg_lead_time_days"]

).round(0)

# Create alerts using the merged inventory_alerts_df

inventory_alerts_df["stockout_risk"] = (
    inventory_alerts_df["quantity_on_hand"] <= 0
)

inventory_alerts_df["low_stock_alert"] = (
    inventory_alerts_df["quantity_on_hand"]
    <
    inventory_alerts_df["reorder_point"]
)

inventory_alerts_df = inventory_alerts_df[
    inventory_alerts_df["stockout_risk"]
    |
    inventory_alerts_df["low_stock_alert"]
]

inventory_alerts_df.to_csv(
    OUTPUT_DIR / "inventory_alerts.csv",
    index=False,
    encoding="utf-8-sig"
)

print(inventory_alerts_df)
print("Inventory alerts created.")

#Freight audit

shipments_df = pd.read_csv(OUTPUT_DIR / "shipment_dataset.csv")

shipments_df["freight_cost"] = pd.to_numeric(
    shipments_df["freight_cost"],
    errors="coerce"
).fillna(0)

avg_freight = shipments_df["freight_cost"].mean()
std_freight = shipments_df["freight_cost"].std()

shipments_df["freight_outlier"] = (
    shipments_df["freight_cost"] > avg_freight + 2 * std_freight
)

freight_audit_df = shipments_df[
    shipments_df["freight_outlier"]
]

freight_audit_df.to_csv(
    OUTPUT_DIR / "freight_audit_exceptions.csv",
    index=False,
    encoding="utf-8-sig"
)

print(freight_audit_df)
print("Freight audit exceptions created.")

# Reconciliation automation

sales_df = pd.read_csv(OUTPUT_DIR / "sales_dataset.csv")
shipments_df = pd.read_csv(OUTPUT_DIR / "shipment_dataset.csv")

sales_by_order = (
    sales_df
    .groupby("order_id", as_index=False)
    .agg(
        sales_revenue=("revenue", "sum"),
        total_units=("quantity", "sum")
    )
)

shipment_orders = (
    shipments_df[["order_id", "shipment_id", "freight_cost"]]
    .drop_duplicates()
)

recon_df = sales_by_order.merge(
    shipment_orders,
    on="order_id",
    how="left"
)

recon_df["missing_shipment"] = recon_df["shipment_id"].isna()

recon_exceptions_df = recon_df[
    recon_df["missing_shipment"]
]

recon_exceptions_df.to_csv(
    OUTPUT_DIR / "reconciliation_exceptions.csv",
    index=False,
    encoding="utf-8-sig"
)

print(recon_exceptions_df)
print("Reconciliation exceptions created.")