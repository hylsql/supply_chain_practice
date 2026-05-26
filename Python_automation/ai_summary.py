import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

# =========================
# READ OUTPUT FILES
# =========================

kpi_df = pd.read_csv(OUTPUT_DIR / "kpi_summary.csv")
inventory_df = pd.read_csv(OUTPUT_DIR / "inventory_dataset.csv")
inventory_alerts_df = pd.read_csv(OUTPUT_DIR / "inventory_alerts.csv")
supplier_df = pd.read_csv(OUTPUT_DIR / "supplier_performance.csv")
po_df = pd.read_csv(OUTPUT_DIR / "purchase_order_dataset.csv")
freight_df = pd.read_csv(OUTPUT_DIR / "freight_audit_exceptions.csv")

summary = []

# =========================
# KPI OVERVIEW
# =========================

inventory_turnover = kpi_df.loc[0, "Inventory Turnover"]
days_on_hand = kpi_df.loc[0, "Days on Hand"]
fill_rate = kpi_df.loc[0, "PO Fill Rate"]
freight_pct = kpi_df.loc[0, "Freight % of Revenue"]
stockout_rate = kpi_df.loc[0, "Stockout Rate"]

summary.append("SUPPLY CHAIN KPI SUMMARY")
summary.append("=" * 40)

summary.append(
    f"Inventory turnover is {inventory_turnover:.2f}x and days on hand is {days_on_hand:.1f} days."
)

if inventory_turnover < 3:
    summary.append("Inventory is moving slowly, which may indicate excess stock or weak demand.")
else:
    summary.append("Inventory turnover appears healthy based on current sales activity.")

if freight_pct > 0.08:
    summary.append(f"Freight cost is elevated at {freight_pct:.2%} of revenue and should be reviewed.")
else:
    summary.append(f"Freight cost is within target range at {freight_pct:.2%} of revenue.")

summary.append(f"PO fill rate is {fill_rate:.2%}.")
summary.append(f"Stockout rate is {stockout_rate:.2%}.")

# =========================
# STOCKOUT RISK
# =========================

summary.append("\nSTOCKOUT RISK")
summary.append("=" * 40)

if not inventory_alerts_df.empty:
    top_stockout = (
        inventory_alerts_df
        .sort_values("reorder_point", ascending=False)
        .head(5)
    )

    summary.append(
        f"{len(inventory_alerts_df)} SKUs are projected to fall below reorder point or are already at stockout risk."
    )

    summary.append("Top stockout-risk SKUs:")

    for _, row in top_stockout.iterrows():
        summary.append(
            f"- {row.get('sku', 'Unknown SKU')}: QOH {row['quantity_on_hand']}, "
            f"reorder point {row['reorder_point']}, "
            f"avg daily sales {row['avg_daily_sales']:.2f}, "
            f"avg lead time {row['avg_lead_time_days']:.1f} days."
        )
else:
    summary.append("No SKUs are currently flagged for stockout risk.")

# =========================
# EXCESS INVENTORY BY WAREHOUSE
# =========================

summary.append("\nEXCESS INVENTORY / WAREHOUSE RISK")
summary.append("=" * 40)

warehouse_inventory = (
    inventory_df
    .groupby("warehouse", as_index=False)
    .agg(
        total_inventory_units=("quantity_on_hand", "sum"),
        total_inventory_value=("inventory_value", "sum")
    )
    .sort_values("total_inventory_value", ascending=False)
)

top_warehouses = warehouse_inventory.head(3)

summary.append("Warehouses with the highest inventory value:")

for _, row in top_warehouses.iterrows():
    summary.append(
        f"- {row['warehouse']}: {row['total_inventory_units']:,.0f} units, "
        f"${row['total_inventory_value']:,.2f} inventory value."
    )

summary.append(
    "High inventory value warehouses may need review for excess stock, slow-moving inventory, or rebalancing opportunities."
)

# =========================
# SUPPLIER PERFORMANCE
# =========================

summary.append("\nSUPPLIER PERFORMANCE")
summary.append("=" * 40)

supplier_df["avg_fill_rate"] = pd.to_numeric(
    supplier_df["avg_fill_rate"],
    errors="coerce"
)

supplier_df["avg_lead_time"] = pd.to_numeric(
    supplier_df["avg_lead_time"],
    errors="coerce"
)

unreliable_suppliers = supplier_df[
    (supplier_df["avg_fill_rate"] < 0.95)
    |
    (supplier_df["avg_lead_time"] > supplier_df["avg_lead_time"].mean())
]

if not unreliable_suppliers.empty:
    summary.append("Suppliers requiring attention:")

    for _, row in unreliable_suppliers.sort_values("avg_fill_rate").head(5).iterrows():
        summary.append(
            f"- {row['supplier_name']}: fill rate {row['avg_fill_rate']:.2%}, "
            f"avg lead time {row['avg_lead_time']:.1f} days, "
            f"total POs {row['total_pos']}."
        )
else:
    summary.append("No major supplier performance issues detected.")

# =========================
# FILL RATE ROOT CAUSE
# =========================

summary.append("\nFILL RATE ANALYSIS")
summary.append("=" * 40)

po_df["fill_rate"] = pd.to_numeric(po_df["fill_rate"], errors="coerce")

low_fill_pos = po_df[po_df["fill_rate"] < 0.95]

if not low_fill_pos.empty:
    supplier_issue = (
        low_fill_pos
        .groupby("supplier_name", as_index=False)
        .agg(
            low_fill_po_count=("po_id", "nunique"),
            avg_fill_rate=("fill_rate", "mean"),
            total_short_qty=("ordered_qty", "sum")
        )
        .sort_values("low_fill_po_count", ascending=False)
        .head(5)
    )

    summary.append(
        f"Fill rate pressure appears to be driven by {len(low_fill_pos)} purchase orders below 95% fill rate."
    )

    summary.append("Main suppliers contributing to low fill rate:")

    for _, row in supplier_issue.iterrows():
        summary.append(
            f"- {row['supplier_name']}: {row['low_fill_po_count']} low-fill POs, "
            f"average fill rate {row['avg_fill_rate']:.2%}."
        )
else:
    summary.append("No purchase orders below 95% fill rate were found.")

# =========================
# FREIGHT AUDIT
# =========================

summary.append("\nFREIGHT AUDIT")
summary.append("=" * 40)

if not freight_df.empty:
    summary.append(
        f"{len(freight_df)} shipments were flagged as freight cost outliers."
    )

    top_freight = freight_df.sort_values("freight_cost", ascending=False).head(5)

    summary.append("Highest freight cost exceptions:")

    for _, row in top_freight.iterrows():
        summary.append(
            f"- Shipment {row['shipment_id']}: carrier {row['carrier']}, "
            f"warehouse {row['ship_from_warehouse']}, "
            f"freight cost ${row['freight_cost']:,.2f}."
        )
else:
    summary.append("No freight cost outliers were detected.")

# =========================
# RECOMMENDATIONS
# =========================

summary.append("\nRECOMMENDATIONS")
summary.append("=" * 40)

if not inventory_alerts_df.empty:
    summary.append("- Review stockout-risk SKUs and prioritize replenishment based on lead time and sales velocity.")

if freight_pct > 0.08 or not freight_df.empty:
    summary.append("- Review freight outliers and carrier charges for possible overbilling or routing inefficiencies.")

if not unreliable_suppliers.empty:
    summary.append("- Follow up with low-performing suppliers and review lead time/fill rate trends.")

summary.append("- Use this report as a daily exception summary for inventory, freight, supplier, and reconciliation risks.")

# =========================
# EXPORT SUMMARY
# =========================

final_summary = "\n".join(summary)

print(final_summary)

with open(
    OUTPUT_DIR / "ai_summary.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(final_summary)

print("AI-style summary created.")
