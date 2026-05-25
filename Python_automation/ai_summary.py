import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

kpi_df = pd.read_csv(
    OUTPUT_DIR / "kpi_summary.csv"
)

inventory_turnover = kpi_df.loc[0, "Inventory Turnover"]
freight_pct = kpi_df.loc[0, "Freight % of Revenue"]

summary = []

if inventory_turnover > 5:
    summary.append(
        "Inventory turnover is healthy."
    )
else:
    summary.append(
        "Inventory turnover may require attention."
    )

if freight_pct > 0.08:
    summary.append(
        "Freight cost percentage is elevated."
    )
else:
    summary.append(
        "Freight costs remain within target range."
    )

final_summary = "\n".join(summary)

print(final_summary)

with open(
    OUTPUT_DIR / "ai_summary.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(final_summary)