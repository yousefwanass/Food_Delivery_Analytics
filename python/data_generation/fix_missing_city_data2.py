"""
Food Delivery Analytics — Gap-Fill Restaurant Orders Fix (Round 2)
====================================================================
The first script (fix_missing_city_data.py) correctly added 121 restaurants:
  - 56 in the 4 new cities (Assiut, Ismailia, Mansoura, Minya) -> got orders
  - 65 cuisine-gap-fill restaurants added to the 6 EXISTING cities
    (Cairo, Tanta, Alexandria, Zagazig, Giza, Sohag) -> got ZERO orders

This script fixes that gap: generates realistic orders (+order_items,
payments, reviews) for those 65 restaurants (IDs 21-85), sized at ~70% of
each city's average per-restaurant order volume among the ORIGINAL 20
restaurants (a newer/smaller-establishment assumption), using the SAME
existing customers/drivers in that city.

Same safety model as before: MAX(id)+1 continuation, append-only,
single transaction, DRY_RUN preview, referential integrity check at the end.

Requires: pip install pyodbc numpy --break-system-packages
"""

import pyodbc
import random
import numpy as np
from datetime import datetime, timedelta

# =====================================================================
SERVER = r"localhost\SQLEXPRESS"          # <-- confirm this matches your instance
DATABASE = "FoodDeliveryAnalytics"       # <-- update to your actual DB name
DRY_RUN = False                             # <-- set to False to actually commit changes

CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
)

random.seed(7)
np.random.seed(7)

GAP_FILL_MIN_ID = 21
GAP_FILL_MAX_ID = 85
NEW_RESTAURANT_SHARE_OF_CITY_AVG = 0.70  # newer entrants assumed at ~70% of established avg

ORDER_STATUS_WEIGHTS = {"Delivered": 0.919, "Cancelled": 0.051, "Failed": 0.030}
PAYMENT_METHODS = ["Card", "Cash", "Wallet"]

CUISINE_CATEGORY_MAP = {
    "Fast Food": ["Burger", "Wrap", "Side", "Drink"],
    "Pizza": ["Pizza", "Side", "Drink"],
    "Burgers": ["Burger", "Side", "Drink"],
    "Desserts": ["Dessert", "Bakery", "Drink", "Coffee"],
    "Cafe": ["Coffee", "Dessert", "Bakery", "Drink"],
    "Bakery": ["Bakery", "Dessert", "Coffee"],
    "Egyptian": ["Main Course", "Side", "Drink", "Chicken"],
}


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

    max_order_id = fetch_scalar(cur, "SELECT MAX(order_id) FROM Orders")
    max_order_item_id = fetch_scalar(cur, "SELECT MAX(order_item_id) FROM Order_Items")
    max_payment_id = fetch_scalar(cur, "SELECT MAX(payment_id) FROM Payments")
    max_review_id = fetch_scalar(cur, "SELECT MAX(review_id) FROM Reviews")
    print(f"Current max IDs -> Order:{max_order_id} OrderItem:{max_order_item_id} "
          f"Payment:{max_payment_id} Review:{max_review_id}")

    # ---- Establish each existing city's average orders-per-restaurant among ORIGINAL restaurants ----
    city_avg = {}
    for row in fetch_all(cur, """
        SELECT r.city, AVG(CAST(oc.order_count AS FLOAT))
        FROM Restaurants r
        JOIN (SELECT restaurant_id, COUNT(*) AS order_count FROM Orders GROUP BY restaurant_id) oc
          ON r.restaurant_id = oc.restaurant_id
        WHERE r.restaurant_id < 21
        GROUP BY r.city
    """):
        city_avg[row[0]] = row[1]
    print(f"City averages (original restaurants): {city_avg}")

    # ---- Gap-fill restaurants and their menu items ----
    gap_restaurants = fetch_all(cur, f"""
        SELECT restaurant_id, cuisine, city FROM Restaurants
        WHERE restaurant_id BETWEEN {GAP_FILL_MIN_ID} AND {GAP_FILL_MAX_ID}
    """)
    menu_by_restaurant = {}
    for row in fetch_all(cur, f"""
        SELECT restaurant_id, item_id, price FROM Menu_Items
        WHERE restaurant_id BETWEEN {GAP_FILL_MIN_ID} AND {GAP_FILL_MAX_ID}
    """):
        menu_by_restaurant.setdefault(row[0], []).append((row[1], row[2]))

    # ---- Existing customers/drivers per city (reuse only, no new ones) ----
    customers_by_city = {}
    for row in fetch_all(cur, "SELECT city, customer_id FROM Customers WHERE city IS NOT NULL"):
        customers_by_city.setdefault(row[0], []).append(row[1])
    drivers_by_city = {}
    for row in fetch_all(cur, "SELECT city, driver_id FROM Drivers WHERE city IS NOT NULL"):
        drivers_by_city.setdefault(row[0], []).append(row[1])

    date_min = datetime(2024, 7, 15, 9, 0, 0)
    date_max = datetime(2026, 7, 15, 20, 0, 0)
    date_span_seconds = int((date_max - date_min).total_seconds())

    new_orders, new_order_items, new_payments, new_reviews = [], [], [], []
    oid_counter = max_order_id
    oiid_counter = max_order_item_id
    pid_counter = max_payment_id
    revid_counter = max_review_id

    for restaurant_id, cuisine, city in gap_restaurants:
        target_orders = int(city_avg.get(city, 800) * NEW_RESTAURANT_SHARE_OF_CITY_AVG)
        city_customers = customers_by_city.get(city, [])
        city_drivers = drivers_by_city.get(city, [])
        items_here = menu_by_restaurant.get(restaurant_id, [])

        if not city_customers or not items_here:
            print(f"WARNING: skipping restaurant {restaurant_id} ({city}) - missing customers/menu items")
            continue

        for _ in range(target_orders):
            oid_counter += 1
            customer_id = random.choice(city_customers)
            driver_id = random.choice(city_drivers) if city_drivers else None
            order_dt = date_min + timedelta(seconds=random.randint(0, date_span_seconds))
            status = random.choices(list(ORDER_STATUS_WEIGHTS.keys()),
                                     weights=list(ORDER_STATUS_WEIGHTS.values()))[0]
            delivery_minutes = max(10, np.random.normal(47.5, 15))
            delivery_dt = order_dt + timedelta(minutes=delivery_minutes)
            payment_method = random.choice(PAYMENT_METHODS)
            delivery_fee = round(random.uniform(15, 35), 0)

            new_orders.append((oid_counter, customer_id, restaurant_id, driver_id,
                                order_dt, delivery_dt, status, payment_method, delivery_fee))

            order_total = 0.0
            for _ in range(random.randint(1, 4)):
                oiid_counter += 1
                item_id, price = random.choice(items_here)
                price = float(price)  # SQL Server DECIMAL comes back as Decimal, not float
                qty = random.randint(1, 3)
                new_order_items.append((oiid_counter, oid_counter, item_id, qty, price))
                order_total += price * qty

            pid_counter += 1
            if status == "Delivered":
                pay_status = "Paid"
            elif status == "Cancelled":
                pay_status = random.choice(["Refunded", "Failed"])
            else:
                pay_status = "Failed"
            new_payments.append((pid_counter, oid_counter, payment_method, pay_status,
                                  round(order_total, 2), order_dt))

            if status == "Delivered" and random.random() < 0.70:
                revid_counter += 1
                rating = round(min(5, max(1, np.random.normal(4.2, 0.7))), 0)
                review_date = delivery_dt + timedelta(days=random.randint(0, 5))
                new_reviews.append((revid_counter, oid_counter, customer_id, restaurant_id,
                                    driver_id, rating, "Great experience overall.", review_date))

    print("\n=== SUMMARY OF ROWS TO INSERT ===")
    print(f"New Orders      : {len(new_orders)}")
    print(f"New Order_Items : {len(new_order_items)}")
    print(f"New Payments    : {len(new_payments)}")
    print(f"New Reviews     : {len(new_reviews)}")

    if DRY_RUN:
        print("\nDRY_RUN = True -> no changes committed. Set DRY_RUN = False to apply.")
        conn.rollback()
        conn.close()
        return

    try:
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

    print("\n=== REFERENTIAL INTEGRITY CHECK ===")
    checks = [
        ("Orphan Orders (restaurant)", "SELECT COUNT(*) FROM Orders o LEFT JOIN Restaurants r ON o.restaurant_id = r.restaurant_id WHERE r.restaurant_id IS NULL"),
        ("Orphan Order_Items (order)", "SELECT COUNT(*) FROM Order_Items oi LEFT JOIN Orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Orphan Payments", "SELECT COUNT(*) FROM Payments p LEFT JOIN Orders o ON p.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Orphan Reviews", "SELECT COUNT(*) FROM Reviews rv LEFT JOIN Orders o ON rv.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("Duplicate Order IDs", "SELECT COUNT(*) FROM (SELECT order_id FROM Orders GROUP BY order_id HAVING COUNT(*) > 1) x"),
        ("Restaurants (21-85) still with zero orders", f"""
            SELECT COUNT(*) FROM Restaurants r
            WHERE r.restaurant_id BETWEEN {GAP_FILL_MIN_ID} AND {GAP_FILL_MAX_ID}
            AND NOT EXISTS (SELECT 1 FROM Orders o WHERE o.restaurant_id = r.restaurant_id)
        """),
    ]
    all_clean = True
    for label, query in checks:
        result = fetch_scalar(cur, query)
        status = "OK" if result == 0 else "FAIL"
        if result != 0:
            all_clean = False
        print(f"  [{status}] {label}: {result}")

    print("\nAll referential integrity checks passed." if all_clean else
          "\nSome checks FAILED - review above.")
    conn.close()


if __name__ == "__main__":
    main()