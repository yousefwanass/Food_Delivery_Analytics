import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

NUM_CUSTOMERS = 3000

cities = {
    "Cairo": 35,
    "Giza": 20,
    "Alexandria": 15,
    "Mansoura": 8,
    "Tanta": 6,
    "Zagazig": 5,
    "Ismailia": 4,
    "Assiut": 3,
    "Minya": 2,
    "Sohag": 2
}

email_domains = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com"
]

phone_prefixes = [
    "010",
    "011",
    "012",
    "015"
]

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    first_name = fake.first_name()
    last_name = fake.last_name()

    gender = random.choice(["Male", "Female"])
    age = random.randint(18, 60)

    city = random.choices(
        population=list(cities.keys()),
        weights=list(cities.values()),
        k=1
    )[0]

    phone = random.choice(phone_prefixes) + "".join(random.choices("0123456789", k=8))

    email = (
        first_name.lower()
        + "."
        + last_name.lower()
        + str(random.randint(1, 999))
        + "@"
        + random.choice(email_domains)
    )

    signup_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    customers.append([
        customer_id,
        first_name,
        last_name,
        gender,
        age,
        phone,
        email,
        city,
        signup_date
    ])


# ===========================
# هنا يبدأ الكود بعد انتهاء الـ Loop
# ===========================

customers_df = pd.DataFrame(
    customers,
    columns=[
        "customer_id",
        "first_name",
        "last_name",
        "gender",
        "age",
        "phone",
        "email",
        "city",
        "signup_date"
    ]
)

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data" / "raw" / "customers.csv"
print(BASE_DIR)
print(OUTPUT_PATH)
customers_df.to_csv(OUTPUT_PATH, index=False)

print("Customers Generated Successfully")