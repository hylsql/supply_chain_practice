from pathlib import Path
import pandas as pd

import os
from dotenv import load_dotenv

import smtplib
from email.message import EmailMessage
from datetime import datetime

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

sales_df = pd.read_csv(OUTPUT_DIR / "sales_dataset.csv")
inventory_analysis_df = pd.read_csv(OUTPUT_DIR / "inventory_dataset.csv")
po_analysis_df = pd.read_csv(OUTPUT_DIR / "purchase_order_dataset.csv")
shipment_analysis_df = pd.read_csv(OUTPUT_DIR / "shipment_dataset.csv")

# convert date columns again after reading CSV
sales_df["order_date"] = pd.to_datetime(sales_df["order_date"], errors="coerce")
po_analysis_df["po_date"] = pd.to_datetime(po_analysis_df["po_date"], errors="coerce")
po_analysis_df["received_date"] = pd.to_datetime(po_analysis_df["received_date"], errors="coerce")
shipment_analysis_df["delivered_date"] = pd.to_datetime(shipment_analysis_df["delivered_date"], errors="coerce")
shipment_analysis_df["promised_delivery_date"] = pd.to_datetime(shipment_analysis_df["promised_delivery_date"], errors="coerce")

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_revenue = sales_df["revenue"].sum()
total_units_sold = sales_df["quantity"].sum()
total_inventory_value = inventory_analysis_df["inventory_value"].sum()

inventory_turnover = (
    sales_df["total_cost"].sum()
    / total_inventory_value
)

days_on_hand = 365 / inventory_turnover

fill_rate = po_analysis_df["fill_rate"].mean()

avg_lead_time = po_analysis_df["lead_time_days"].mean()

freight_pct_revenue = (
    shipment_analysis_df["freight_cost"].sum()
    / total_revenue
)

stockout_rate = (
    inventory_analysis_df[
        inventory_analysis_df["quantity_on_hand"] == 0
    ]["product_id"].nunique()
    / inventory_analysis_df["product_id"].nunique()
)

on_time_delivery_rate = (
    shipment_analysis_df["on_time_flag"].mean()
)

# ==========================================
# ABC ANALYSIS
# ==========================================

abc_df = (
    sales_df
    .groupby(["product_id", "sku", "product_name"], as_index=False)
    ["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)

abc_df["revenue_pct"] = (
    abc_df["revenue"] / abc_df["revenue"].sum()
)

abc_df["cumulative_pct"] = (
    abc_df["revenue_pct"].cumsum()
)

def assign_abc(row):
    if row["cumulative_pct"] <= 0.80:
        return "A"
    elif row["cumulative_pct"] <= 0.95:
        return "B"
    else:
        return "C"

abc_df["abc_class"] = abc_df.apply(assign_abc, axis=1)

# ==========================================
# SUPPLIER PERFORMANCE
# ==========================================

supplier_performance_df = (
    po_analysis_df
    .groupby("supplier_name", as_index=False)
    .agg(
        total_pos=("po_id", "nunique"),
        avg_lead_time=("lead_time_days", "mean"),
        avg_fill_rate=("fill_rate", "mean"),
        total_ordered_qty=("ordered_qty", "sum"),
        total_received_qty=("received_qty", "sum")
    )
)

# ==========================================
# KPI SUMMARY TABLE
# ==========================================

kpi_summary_df = pd.DataFrame([{
    "Total Revenue": total_revenue,
    "Total Units Sold": total_units_sold,
    "Inventory Value": total_inventory_value,
    "Inventory Turnover": inventory_turnover,
    "Days on Hand": days_on_hand,
    "PO Fill Rate": fill_rate,
    "Average Lead Time": avg_lead_time,
    "Freight % of Revenue": freight_pct_revenue,
    "Stockout Rate": stockout_rate,
    "On-Time Delivery Rate": on_time_delivery_rate
}])

print(kpi_summary_df)

# ==========================================
# EXPORT OUTPUTS
# ==========================================

sales_df.to_csv(
    OUTPUT_DIR / "sales_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

inventory_analysis_df.to_csv(
    OUTPUT_DIR / "inventory_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

po_analysis_df.to_csv(
    OUTPUT_DIR / "purchase_order_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

shipment_analysis_df.to_csv(
    OUTPUT_DIR / "shipment_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

abc_df.to_csv(
    OUTPUT_DIR / "abc_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

supplier_performance_df.to_csv(
    OUTPUT_DIR / "supplier_performance.csv",
    index=False,
    encoding="utf-8-sig"
)

kpi_summary_df.to_csv(
    OUTPUT_DIR / "kpi_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Supply chain KPI datasets exported successfully.")

# ==========================================
# LOAD EMAIL.ENV FILE
# ==========================================

ENV_PATH = Path(__file__).parent / "email.env"
load_dotenv(ENV_PATH)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ==========================================
# EMAIL KPI SUMMARY
# ==========================================


today = datetime.today().strftime("%Y-%m-%d")

msg = EmailMessage()

msg["Subject"] = f"Supply Chain KPI Report - {today}"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

msg.set_content(f"""
Hi,

Your automated Supply Chain KPI report is ready.

KPI Summary:
- Total Revenue: ${total_revenue:,.2f}
- Total Units Sold: {total_units_sold:,.0f}
- Inventory Value: ${total_inventory_value:,.2f}
- Inventory Turnover: {inventory_turnover:.2f}
- Days on Hand: {days_on_hand:.1f}
- PO Fill Rate: {fill_rate:.2%}
- Average Lead Time: {avg_lead_time:.1f} days
- Freight % of Revenue: {freight_pct_revenue:.2%}
- Stockout Rate: {stockout_rate:.2%}
- On-Time Delivery Rate: {on_time_delivery_rate:.2%}

Generated files are saved in your output folder.

Best,
Python Supply Chain Automation
""")

# Attach KPI summary CSV
kpi_file = OUTPUT_DIR / "kpi_summary.csv"

with open(kpi_file, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="text",
        subtype="csv",
        filename=kpi_file.name
    )

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(
        EMAIL_SENDER.strip(),
        EMAIL_PASSWORD.replace(" ", "").strip()
    )

    smtp.send_message(msg)

print("KPI summary email sent successfully.")