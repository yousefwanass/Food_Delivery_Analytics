import pandas as pd
import pyodbc
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=BrazilianEcommerce;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.fast_executemany = True

# الترتيب مهم عشان الـ Foreign Keys (الجداول الأب الأول)
tables = [
    ("customers", "olist_customers_dataset.csv"),
    ("sellers", "olist_sellers_dataset.csv"),
    ("geolocation", "olist_geolocation_dataset.csv"),
    ("product_category_name_translation", "product_category_name_translation.csv"),
    ("products", "olist_products_dataset.csv"),
    ("orders", "olist_orders_dataset.csv"),
    ("order_items", "olist_order_items_dataset.csv"),
    ("order_payments", "olist_order_payments_dataset.csv"),
    ("order_reviews", "olist_order_reviews_dataset.csv"),
]

for table, file in tables:

    print(f"Loading {table}...")

    df = pd.read_csv(DATA_DIR / file)

    # يستبدل NaN بـ None عشان SQL Server يقبلها NULL بدل ما يرفض القيمة
    df = df.where(pd.notnull(df), None)

    columns = ",".join(df.columns)
    placeholders = ",".join(["?"] * len(df.columns))

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    data = list(df.itertuples(index=False, name=None))
    cursor.executemany(sql, data)

    conn.commit()

    print(f"{table} Done ({len(df)} rows)")

cursor.close()
conn.close()

print("Finished Successfully")