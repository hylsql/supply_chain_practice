from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

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
# SQL REPORTS
# ==========================================

top_products_query = """
SELECT
    product_id,
    SUM(quantity) AS total_units_sold
FROM order_items
GROUP BY product_id
ORDER BY total_units_sold DESC
LIMIT 10;
"""

top_products_df = pd.read_sql(
    top_products_query,
    engine
)

top_products_df.to_csv(
    OUTPUT_DIR / "top_products_report.csv",
    index=False,
    encoding="utf-8-sig"
)

print("SQL reports generated.")
print(top_products_df)