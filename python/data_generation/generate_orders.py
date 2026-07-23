import pandas as pd
import random
from pathlib import Path
from faker import Faker
from datetime import timedelta

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[2]

NUM_ORDERS = 25000

# ==========================
# Read Data
# ==========================

customers = pd.read_csv(BASE_DIR / "data" / "raw" / "customers.csv")
restaurants = pd.read_csv(BASE_DIR / "data" / "raw" / "restaurants.csv")
drivers = pd.read_csv(BASE_DIR / "data" / "raw" / "drivers.csv")

orders = []

# ==========================
# Helper Functions
# ==========================

def get_random_customer():
    return customers.sample(1).iloc[0]


def get_restaurants_by_city(city):
    return restaurants[restaurants["city"] == city]


def get_drivers_by_city(city):
    return drivers[
        (drivers["city"] == city) &
        (drivers["status"] == "Active")
    ]


# ==========================
# Generate Orders
# ==========================

order_id = 1

while order_id <= NUM_ORDERS:

    customer = get_random_customer()
    customer_city = customer["city"]

    available_restaurants = get_restaurants_by_city(customer_city)
    available_drivers = get_drivers_by_city(customer_city)

    if available_restaurants.empty or available_drivers.empty:
        continue

    restaurant = available_restaurants.sample(1).iloc[0]
    driver = available_drivers.sample(1).iloc[0]

    order_datetime = fake.date_time_between(
        start_date="-2y",
        end_date="now"
    )

    delivery_minutes = random.randint(20, 75)

    delivery_datetime = order_datetime + timedelta(
        minutes=delivery_minutes
    )

    order_status = random.choices(
        ["Delivered", "Cancelled", "Failed"],
        weights=[92, 5, 3],
        k=1
    )[0]

    payment_method = random.choices(
        ["Cash", "Card", "Wallet"],
        weights=[45, 40, 15],
        k=1
    )[0]

    delivery_fee = random.choice(
        [15, 20, 25, 30, 35]
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer["customer_id"],
        "restaurant_id": restaurant["restaurant_id"],
        "driver_id": driver["driver_id"],
        "order_datetime": order_datetime,
        "delivery_datetime": delivery_datetime,
        "order_status": order_status,
        "payment_method": payment_method,
        "delivery_fee": delivery_fee
    })

    order_id += 1

# ==========================
# Save CSV
# ==========================

orders_df = pd.DataFrame(orders)

output_path = BASE_DIR / "data" / "raw" / "orders.csv"

orders_df.to_csv(output_path, index=False)

print("Orders Generated Successfully")