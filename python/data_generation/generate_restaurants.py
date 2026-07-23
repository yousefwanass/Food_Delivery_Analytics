import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

seed_path = BASE_DIR / "data" / "raw" / "restaurants_seed.csv"

restaurants = pd.read_csv(seed_path)

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

restaurant_data = []

for index, row in restaurants.iterrows():

    restaurant_data.append({
        "restaurant_id": index + 1,
        "restaurant_name": row["restaurant_name"],
        "cuisine": row["cuisine"],
        "city": random.choices(
            population=list(cities.keys()),
            weights=list(cities.values()),
            k=1
        )[0],
        "rating": round(random.uniform(3.5, 5.0), 1),
        "opening_time": "10:00",
        "closing_time": random.choice([
            "22:00",
            "23:00",
            "00:00",
            "01:00"
        ])
    })

restaurants_df = pd.DataFrame(restaurant_data)

output_path = BASE_DIR / "data" / "raw" / "restaurants.csv"

restaurants_df.to_csv(output_path, index=False)

print("Restaurants Generated Successfully")