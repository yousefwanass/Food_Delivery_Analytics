"""
Food Delivery Analytics — Source Data Fix
==========================================
Adds missing Restaurants (+ downstream Menu_Items, Orders, Order_Items,
Payments, Reviews) for Assiut, Ismailia, Mansoura, and Minya, and fills
cuisine gaps across ALL 10 cities so every city has balanced cuisine coverage.

DOES NOT touch, update, or delete any existing row. Only appends new rows,
with IDs continuing from MAX(id)+1 in each table — fully preserves referential
integrity and every existing relationship/ID.

Verified facts this script relies on (pulled live from your model before writing this):
  - Cuisines in use: Fast Food, Pizza, Burgers, Desserts, Cafe, Bakery, Egyptian
  - Menu_Items categories: Burger, Wrap, Side, Chicken, Drink, Dessert, Pizza, Main Course, Coffee, Bakery
  - Menu_Items price range: 32 - 278 (avg ~104)
  - Restaurant rating range: 3.6 - 4.9
  - Order statuses: Delivered (91.9%), Cancelled (5.1%), Failed (3.0%)
  - Payment methods: Card, Cash, Wallet
  - Payment statuses: Paid, Refunded, Failed
  - Order date range: 2024-07-15 to 2026-07-15
  - Delivery fee range: 15 - 35
  - Orders-per-customer ratio across existing cities: ~9.75 to ~10.8 (used to size new-city order volume realistically)

Requires: pip install pyodbc pandas numpy --break-system-packages
"""

import pyodbc
import random
import numpy as np
from datetime import datetime, timedelta

# =====================================================================
# CONFIG — update these two lines to match your environment
# =====================================================================
SERVER = r"localhost\SQLEXPRESS"          # <-- confirm this matches your instance
DATABASE = "FoodDeliveryAnalytics"       # <-- update to your actual DB name
DRY_RUN = False                             # <-- set to False to actually commit changes

CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
)

random.seed(42)
np.random.seed(42)

CUISINES = ["Fast Food", "Pizza", "Burgers", "Desserts", "Cafe", "Bakery", "Egyptian"]
TARGET_RESTAURANTS_PER_CUISINE = 2  # -> 14 restaurants per fully-built city

NEW_CITIES = ["Assiut", "Ismailia", "Mansoura", "Minya"]
ALL_CITIES = ["Cairo", "Tanta", "Alexandria", "Zagazig", "Giza", "Sohag"] + NEW_CITIES

ORDERS_PER_CUSTOMER_RATIO = 10.0  # matches empirical ~9.75-10.8 across existing cities

ORDER_STATUS_WEIGHTS = {"Delivered": 0.919, "Cancelled": 0.051, "Failed": 0.030}
PAYMENT_METHODS = ["Card", "Cash", "Wallet"]

# Cuisine -> plausible menu categories, for realistic item generation
CUISINE_CATEGORY_MAP = {
    "Fast Food": ["Burger", "Wrap", "Side", "Drink"],
    "Pizza": ["Pizza", "Side", "Drink"],
    "Burgers": ["Burger", "Side", "Drink"],
    "Desserts": ["Dessert", "Bakery", "Drink", "Coffee"],
    "Cafe": ["Coffee", "Dessert", "Bakery", "Drink"],
    "Bakery": ["Bakery", "Dessert", "Coffee"],
    "Egyptian": ["Main Course", "Side", "Drink", "Chicken"],
}

ITEM_NAME_POOL = {
    "Burger": ["Classic Beef Burger", "Cheese Burger", "Double Smash Burger", "Chicken Burger"],
    "Wrap": ["Chicken Shawarma Wrap", "Falafel Wrap", "Grilled Veggie Wrap"],
    "Side": ["French Fries", "Onion Rings", "Garlic Bread", "Coleslaw"],
    "Chicken": ["Grilled Chicken Plate", "Fried Chicken Bucket", "Chicken Tikka"],
    "Drink": ["Soft Drink", "Fresh Lemonade", "Iced Tea", "Mineral Water"],
    "Dessert": ["Chocolate Cake", "Baklava", "Cheesecake", "Kunafa"],
    "Pizza": ["Margherita Pizza", "Pepperoni Pizza", "Vegetable Pizza", "Four Cheese Pizza"],
    "Main Course": ["Koshary", "Molokhia with Rice", "Grilled Kofta", "Stuffed Pigeon"],
    "Coffee": ["Espresso", "Cappuccino", "Turkish Coffee", "Iced Latte"],
    "Bakery": ["Croissant", "Feteer Meshaltet", "Baladi Bread Basket"],
}

RESTAURANT_NAME_TEMPLATES = [
    "{city} {cuisine} House", "Al {city} {cuisine}", "{cuisine} Corner - {city}",
    "The {cuisine} Spot", "{city} Bites", "Golden {cuisine}", "{cuisine} Palace",
]


def get_conn():
    return pyodbc.connect(CONN_STR)


def fetch_scalar(cur, query):
    cur.execute(query)
    row = cur.fetchone()
    return row[0] if row and row[0] is not None else 0


def fetch_all(cur, query):
    cur.execute(query)
    return cur.fetchall()


def main():
    conn = get_conn()
    conn.autocommit = False
    cur = conn.cursor()

    # ---- 1. Read current max IDs (preserve everything existing) ----
    max_restaurant_id = fetch_scalar(cur, "SELECT MAX(restaurant_id) FROM Restaurants")
    max_item_id = fetch_scalar(cur, "SELECT MAX(item_id) FROM Menu_Items")
    max_order_id = fetch_scalar(cur, "SELECT MAX(order_id) FROM Orders")
    max_order_item_id = fetch_scalar(cur, "SELECT MAX(order_item_id) FROM Order_Items")
    max_payment_id = fetch_scalar(cur, "SELECT MAX(payment_id) FROM Payments")
    max_review_id = fetch_scalar(cur, "SELECT MAX(review_id) FROM Reviews")

    print(f"Current max IDs -> Restaurant:{max_restaurant_id} Item:{max_item_id} "
          f"Order:{max_order_id} OrderItem:{max_order_item_id} "
          f"Payment:{max_payment_id} Review:{max_review_id}")

    # ---- 2. Determine existing cuisine coverage per city ----
    existing_coverage = {}
    for row in fetch_all(cur, "SELECT city, cuisine, COUNT(*) FROM Restaurants GROUP BY city, cuisine"):
        city, cuisine, cnt = row
        existing_coverage.setdefault(city, {})[cuisine] = cnt

    # ---- 3. Existing customers/drivers per city (reuse — do NOT create new ones) ----
    customers_by_city = {}
    for row in fetch_all(cur, "SELECT city, customer_id FROM Customers WHERE city IS NOT NULL"):
        customers_by_city.setdefault(row[0], []).append(row[1])

    drivers_by_city = {}
    for row in fetch_all(cur, "SELECT city, driver_id FROM Drivers WHERE city IS NOT NULL"):
        drivers_by_city.setdefault(row[0], []).append(row[1])

    date_min = datetime(2024, 7, 15, 9, 0, 0)
    date_max = datetime(2026, 7, 15, 20, 0, 0)
    date_span_seconds = int((date_max - date_min).total_seconds())

    new_restaurants = []   # (restaurant_id, name, cuisine, city, rating, opening, closing)
    new_menu_items = []    # (item_id, restaurant_id, item_name, category, price)
    new_orders = []        # (order_id, customer_id, restaurant_id, driver_id, order_dt, delivery_dt, status, payment_method, delivery_fee)
    new_order_items = []   # (order_item_id, order_id, item_id, quantity, unit_price)
    new_payments = []      # (payment_id, order_id, payment_method, payment_status, amount_paid, payment_dt)
    new_reviews = []       # (review_id, order_id, customer_id, restaurant_id, driver_id, rating, review_text, review_date)

    rid_counter = max_restaurant_id
    iid_counter = max_item_id
    oid_counter = max_order_id
    oiid_counter = max_order_item_id
    pid_counter = max_payment_id
    revid_counter = max_review_id

    restaurants_by_city_for_orders = {}  # city -> list of restaurant_ids (existing + new) used for order generation

    # ---- 4. Fill cuisine gaps for ALL cities (existing + new) ----
    for city in ALL_CITIES:
        coverage = existing_coverage.get(city, {})
        restaurants_by_city_for_orders.setdefault(city, [])

        for cuisine in CUISINES:
            have = coverage.get(cuisine, 0)
            need = max(0, TARGET_RESTAURANTS_PER_CUISINE - have)
            for _ in range(need):
                rid_counter += 1
                name_template = random.choice(RESTAURANT_NAME_TEMPLATES)
                name = name_template.format(city=city, cuisine=cuisine)
                rating = round(random.uniform(3.6, 4.9), 1)
                opening = datetime(1900, 1, 1, random.choice([7, 8, 9, 10]), 0, 0)
                closing = datetime(1900, 1, 1, random.choice([22, 23]), random.choice([0, 30]), 0)
                new_restaurants.append((rid_counter, name, cuisine, city, rating, opening, closing))
                restaurants_by_city_for_orders[city].append(rid_counter)

                # menu items for this new restaurant
                categories = CUISINE_CATEGORY_MAP[cuisine]
                for _ in range(8):
                    iid_counter += 1
                    category = random.choice(categories)
                    item_name = random.choice(ITEM_NAME_POOL[category])
                    price = round(np.random.normal(104, 45), 0)
                    price = max(32, min(278, price))
                    new_menu_items.append((iid_counter, rid_counter, item_name, category, price))

    # ---- 5. Generate ORDERS only for the 4 target cities (the stated gap) ----
    for city in NEW_CITIES:
        city_customers = customers_by_city.get(city, [])
        city_drivers = drivers_by_city.get(city, [])
        city_restaurants = restaurants_by_city_for_orders.get(city, [])

        if not city_customers or not city_restaurants:
            print(f"WARNING: skipping {city} - missing customers or restaurants")
            continue

        target_orders = int(len(city_customers) * ORDERS_PER_CUSTOMER_RATIO)
        print(f"{city}: {len(city_customers)} customers -> generating {target_orders} orders "
              f"across {len(city_restaurants)} new restaurants")

        # pre-index menu items per restaurant for order_items generation
        menu_by_restaurant = {}
        for (iid, rid, name, cat, price) in new_menu_items:
            if rid in city_restaurants:
                menu_by_restaurant.setdefault(rid, []).append((iid, price))

        for _ in range(target_orders):
            oid_counter += 1
            customer_id = random.choice(city_customers)
            restaurant_id = random.choice(city_restaurants)
            driver_id = random.choice(city_drivers) if city_drivers else None

            order_dt = date_min + timedelta(seconds=random.randint(0, date_span_seconds))
            status = random.choices(list(ORDER_STATUS_WEIGHTS.keys()),
                                     weights=list(ORDER_STATUS_WEIGHTS.values()))[0]

            # delivery_datetime is NOT NULL in the actual SQL schema - existing data
            # confirms even Cancelled/Failed orders have it populated (order_dt + ~45-90 min)
            delivery_minutes = max(10, np.random.normal(47.5, 15))
            delivery_dt = order_dt + timedelta(minutes=delivery_minutes)

            payment_method = random.choice(PAYMENT_METHODS)
            delivery_fee = round(random.uniform(15, 35), 0)

            new_orders.append((oid_counter, customer_id, restaurant_id, driver_id,
                                order_dt, delivery_dt, status, payment_method, delivery_fee))

            # order items (1-4 line items from this restaurant's menu)
            items_here = menu_by_restaurant.get(restaurant_id, [])
            order_total = 0.0
            if items_here:
                n_items = random.randint(1, 4)
                for _ in range(n_items):
                    oiid_counter += 1
                    item_id, price = random.choice(items_here)
                    qty = random.randint(1, 3)
                    new_order_items.append((oiid_counter, oid_counter, item_id, qty, price))
                    order_total += price * qty

            # payment
            pid_counter += 1
            if status == "Delivered":
                pay_status = "Paid"
            elif status == "Cancelled":
                pay_status = random.choice(["Refunded", "Failed"])
            else:
                pay_status = "Failed"
            new_payments.append((pid_counter, oid_counter, payment_method, pay_status,
                                  round(order_total, 2), order_dt))

            # review (~70% of delivered orders)
            if status == "Delivered" and random.random() < 0.70:
                revid_counter += 1
                rating = round(min(5, max(1, np.random.normal(4.2, 0.7))), 0)
                review_date = delivery_dt + timedelta(days=random.randint(0, 5))
                new_reviews.append((revid_counter, oid_counter, customer_id, restaurant_id,
                                    driver_id, rating, "Great experience overall.", review_date))

    # ---- 6. Summary ----
    print("\n=== SUMMARY OF ROWS TO INSERT ===")
    print(f"New Restaurants : {len(new_restaurants)}")
    print(f"New Menu_Items  : {len(new_menu_items)}")
    print(f"New Orders      : {len(new_orders)}")
    print(f"New Order_Items : {len(new_order_items)}")
    print(f"New Payments    : {len(new_payments)}")
    print(f"New Reviews     : {len(new_reviews)}")

    if DRY_RUN:
        print("\nDRY_RUN = True -> no changes committed. Set DRY_RUN = False to apply.")
        conn.rollback()
        conn.close()
        return

    # ---- 7. Insert everything inside a single transaction ----
    try:
        cur.executemany(
            "INSERT INTO Restaurants (restaurant_id, restaurant_name, cuisine, city, rating, opening_time, closing_time) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)", new_restaurants)

        cur.executemany(
            "INSERT INTO Menu_Items (item_id, restaurant_id, item_name, category, price) "
            "VALUES (?, ?, ?, ?, ?)", new_menu_items)

        cur.executemany(
            "INSERT INTO Orders (order_id, customer_id, restaurant_id, driver_id, order_datetime, "
            "delivery_datetime, order_status, payment_method, delivery_fee) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", new_orders)

        cur.executemany(
            "INSERT INTO Order_Items (order_item_id, order_id, item_id, quantity, unit_price) "
            "VALUES (?, ?, ?, ?, ?)", new_order_items)

        cur.executemany(
            "INSERT INTO Payments (payment_id, order_id, payment_method, payment_status, amount_paid, payment_datetime) "
            "VALUES (?, ?, ?, ?, ?, ?)", new_payments)

        cur.executemany(
            "INSERT INTO Reviews (review_id, order_id, customer_id, restaurant_id, driver_id, rating, review_text, review_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", new_reviews)

        conn.commit()
        print("\nAll inserts committed successfully.")

    except Exception as e:
        conn.rollback()
        print(f"\nERROR - rolled back all changes: {e}")
        raise

    # ---- 8. Referential integrity verification ----
    print("\n=== REFERENTIAL INTEGRITY CHECK ===")
    checks = [
        ("Orphan Menu_Items", "SELECT COUNT(*) FROM Menu_Items m LEFT JOIN Restaurants r ON m.restaurant_id = r.restaurant_id WHERE r.restaurant_id IS NULL"),
        ("Orphan Orders (restaurant)", "SELECT COUNT(*) FROM Orders o LEFT JOIN Restaurants r ON o.restaurant_id = r.restaurant_id WHERE r.restaurant_id IS NULL"),
        ("Orphan Orders (customer)", "SELECT COUNT(*) FROM Orders o LEFT JOIN Customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL"),
        ("Orphan Order_Items (order)", "SELECT COUNT(*) FROM Order_Items oi LEFT JOIN Orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Orphan Order_Items (item)", "SELECT COUNT(*) FROM Order_Items oi LEFT JOIN Menu_Items m ON oi.item_id = m.item_id WHERE m.item_id IS NULL"),
        ("Orphan Payments", "SELECT COUNT(*) FROM Payments p LEFT JOIN Orders o ON p.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Orphan Reviews", "SELECT COUNT(*) FROM Reviews rv LEFT JOIN Orders o ON rv.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Duplicate Restaurant IDs", "SELECT COUNT(*) FROM (SELECT restaurant_id FROM Restaurants GROUP BY restaurant_id HAVING COUNT(*) > 1) x"),
        ("Duplicate Order IDs", "SELECT COUNT(*) FROM (SELECT order_id FROM Orders GROUP BY order_id HAVING COUNT(*) > 1) x"),
    ]
    all_clean = True
    for label, query in checks:
        result = fetch_scalar(cur, query)
        status = "OK" if result == 0 else "FAIL"
        if result != 0:
            all_clean = False
        print(f"  [{status}] {label}: {result}")

    print("\nAll referential integrity checks passed." if all_clean else
          "\nSome checks FAILED - review above before trusting the refreshed dataset.")

    conn.close()


if __name__ == "__main__":
    main()
