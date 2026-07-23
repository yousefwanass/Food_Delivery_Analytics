import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[2]

NUM_DRIVERS = 400

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

vehicle_types = [
    "Motorcycle",
    "Scooter",
    "Car",
    "Bicycle"
]

vehicle_weights = [
    60,
    20,
    10,
    10
]

statuses = [
    "Active",
    "Inactive",
    "On Leave"
]

status_weights = [
    85,
    10,
    5
]

phone_prefixes = [
    "010",
    "011",
    "012",
    "015"
]

drivers = []
for driver_id in range(1, NUM_DRIVERS + 1):

    first_name = fake.first_name()

    last_name = fake.last_name()

    gender = random.choice(["Male", "Female"])

    age = random.randint(21, 55)

    phone = random.choice(phone_prefixes) + "".join(
        random.choices("0123456789", k=8)
    )

    city = random.choices(
        list(cities.keys()),
        weights=list(cities.values()),
        k=1
    )[0]

    vehicle = random.choices(
        vehicle_types,
        weights=vehicle_weights,
        k=1
    )[0]

    rating = round(random.uniform(3.8, 5.0), 1)

    joining_date = fake.date_between(
        start_date="-4y",
        end_date="today"
    )

    status = random.choices(
        statuses,
        weights=status_weights,
        k=1
    )[0]

    drivers.append({

        "driver_id": driver_id,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "phone": phone,
        "city": city,
        "vehicle_type": vehicle,
        "rating": rating,
        "joining_date": joining_date,
        "status": status

    })
drivers_df = pd.DataFrame(drivers)

output_path = BASE_DIR / "data" / "raw" / "drivers.csv"

drivers_df.to_csv(output_path, index=False)

print("Drivers Generated Successfully")
    