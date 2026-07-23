import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw"

# ==========================
# Read Data
# ==========================

customers = pd.read_csv(DATA_PATH / "customers.csv")
restaurants = pd.read_csv(DATA_PATH / "restaurants.csv")
drivers = pd.read_csv(DATA_PATH / "drivers.csv")
menu_items = pd.read_csv(DATA_PATH / "menu_items.csv")
orders = pd.read_csv(DATA_PATH / "orders.csv")
order_items = pd.read_csv(DATA_PATH / "order_items.csv")
payments = pd.read_csv(DATA_PATH / "payments.csv")
reviews = pd.read_csv(DATA_PATH / "reviews.csv")

print("=" * 60)
print("FOOD DELIVERY DATA VALIDATION REPORT")
print("=" * 60)

# ==========================
# Missing Values
# ==========================

print("\nMissing Values")
print("-" * 60)

tables = {
    "Customers": customers,
    "Restaurants": restaurants,
    "Drivers": drivers,
    "Menu Items": menu_items,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews
}

for name, df in tables.items():
    missing = df.isnull().sum().sum()
    print(f"{name}: {missing}")

# ==========================
# Duplicate Primary Keys
# ==========================

print("\nDuplicate IDs")
print("-" * 60)

checks = [
    ("Customers", customers, "customer_id"),
    ("Restaurants", restaurants, "restaurant_id"),
    ("Drivers", drivers, "driver_id"),
    ("Menu Items", menu_items, "item_id"),
    ("Orders", orders, "order_id"),
    ("Order Items", order_items, "order_item_id"),
    ("Payments", payments, "payment_id"),
    ("Reviews", reviews, "review_id")
]

for table, df, key in checks:

    duplicates = df[key].duplicated().sum()

    print(f"{table}: {duplicates}")

# ==========================
# Foreign Keys
# ==========================

print("\nForeign Key Validation")
print("-" * 60)

print(
    "Orders -> Customers:",
    (~orders["customer_id"].isin(customers["customer_id"])).sum()
)

print(
    "Orders -> Restaurants:",
    (~orders["restaurant_id"].isin(restaurants["restaurant_id"])).sum()
)

print(
    "Orders -> Drivers:",
    (~orders["driver_id"].isin(drivers["driver_id"])).sum()
)

print(
    "Menu Items -> Restaurants:",
    (~menu_items["restaurant_id"].isin(restaurants["restaurant_id"])).sum()
)

print(
    "Order Items -> Orders:",
    (~order_items["order_id"].isin(orders["order_id"])).sum()
)

print(
    "Order Items -> Menu Items:",
    (~order_items["item_id"].isin(menu_items["item_id"])).sum()
)

print(
    "Payments -> Orders:",
    (~payments["order_id"].isin(orders["order_id"])).sum()
)

print(
    "Reviews -> Orders:",
    (~reviews["order_id"].isin(orders["order_id"])).sum()
)

# ==========================
# Business Rules
# ==========================

print("\nBusiness Rules")
print("-" * 60)

orders_without_items = (
    ~orders["order_id"].isin(order_items["order_id"])
).sum()

print("Orders without items:", orders_without_items)

cancelled_reviews = reviews.merge(
    orders[["order_id", "order_status"]],
    on="order_id"
)

cancelled_reviews = cancelled_reviews[
    cancelled_reviews["order_status"] != "Delivered"
]

print("Reviews for non-delivered orders:", len(cancelled_reviews))

print("\nValidation Finished Successfully")
print("=" * 60)