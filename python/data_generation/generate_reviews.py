import pandas as pd
import random
from pathlib import Path
from faker import Faker

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[2]

orders = pd.read_csv(BASE_DIR / "data" / "raw" / "orders.csv")

reviews = []

review_id = 1

positive_reviews = [
    "Excellent service",
    "Very fast delivery",
    "Food was delicious",
    "Highly recommended",
    "Fresh food",
    "Driver was polite",
    "Perfect experience",
    "Amazing restaurant"
]

negative_reviews = [
    "Late delivery",
    "Cold food",
    "Wrong order",
    "Average experience",
    "Food quality could be better",
    "Driver was rude",
    "Not worth the price",
    "Poor packaging"
]

for _, order in orders.iterrows():

    if order["order_status"] != "Delivered":
        continue

    if random.random() > 0.65:
        continue

    rating = random.choices(
        [5,4,3,2,1],
        weights=[45,30,15,7,3],
        k=1
    )[0]

    if rating >= 4:
        review = random.choice(positive_reviews)
    else:
        review = random.choice(negative_reviews)

    reviews.append({

        "review_id": review_id,

        "order_id": order["order_id"],

        "customer_id": order["customer_id"],

        "restaurant_id": order["restaurant_id"],

        "driver_id": order["driver_id"],

        "rating": rating,

        "review_text": review,

        "review_date": order["delivery_datetime"]

    })

    review_id += 1

reviews_df = pd.DataFrame(reviews)

reviews_df.to_csv(
    BASE_DIR / "data" / "raw" / "reviews.csv",
    index=False
)

print("Reviews Generated Successfully")