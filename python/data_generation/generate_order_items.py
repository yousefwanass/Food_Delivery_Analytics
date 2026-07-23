import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# ==========================
# Read Data
# ==========================

orders = pd.read_csv(BASE_DIR / "data" / "raw" / "orders.csv")
menu_items = pd.read_csv(BASE_DIR / "data" / "raw" / "menu_items.csv")

order_items = []

order_item_id = 1

# ==========================
# Generate Order Items
# ==========================

for _, order in orders.iterrows():

    restaurant_id = order["restaurant_id"]

    restaurant_menu = menu_items[
        menu_items["restaurant_id"] == restaurant_id
    ]

    number_of_items = random.randint(1, 5)

    selected_items = restaurant_menu.sample(
        n=min(number_of_items, len(restaurant_menu)),
        replace=False
    )

    for _, item in selected_items.iterrows():

        quantity = random.randint(1, 3)

        order_items.append({

            "order_item_id": order_item_id,

            "order_id": order["order_id"],

            "item_id": item["item_id"],

            "quantity": quantity,

            "unit_price": item["price"]

        })

        order_item_id += 1

# ==========================
# Save CSV
# ==========================

order_items_df = pd.DataFrame(order_items)

output_path = BASE_DIR / "data" / "raw" / "order_items.csv"

order_items_df.to_csv(output_path, index=False)

print("Order Items Generated Successfully")