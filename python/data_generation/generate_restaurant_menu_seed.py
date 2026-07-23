import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

restaurants_path = BASE_DIR / "data" / "raw" / "restaurants_seed.csv"

restaurants = pd.read_csv(restaurants_path)

menu_templates = {

    "Fast Food": [
        ("Big Mac", "Burger", 145),
        ("McChicken", "Burger", 135),
        ("Chicken Burger", "Burger", 120),
        ("Fries", "Side", 55),
        ("Cola", "Drink", 35),
        ("Nuggets", "Chicken", 95),
        ("Chicken Wings", "Chicken", 140),
        ("Mozzarella Sticks", "Side", 85),
        ("Chicken Wrap", "Wrap", 125),
        ("Ice Cream", "Dessert", 55),
    ],

    "Pizza": [
        ("Pepperoni Pizza", "Pizza", 220),
        ("Margherita Pizza", "Pizza", 180),
        ("Chicken Ranch", "Pizza", 240),
        ("BBQ Chicken Pizza", "Pizza", 260),
        ("Garlic Bread", "Side", 75),
        ("Cheese Sticks", "Side", 95),
        ("Pepsi", "Drink", 35),
        ("7UP", "Drink", 35),
        ("Chocolate Lava", "Dessert", 95),
        ("Tiramisu", "Dessert", 120),
    ],

    "Burgers": [
        ("Classic Burger", "Burger", 160),
        ("Cheese Burger", "Burger", 175),
        ("Mushroom Burger", "Burger", 190),
        ("Loaded Fries", "Side", 90),
        ("Onion Rings", "Side", 70),
        ("Cola", "Drink", 35),
        ("Milkshake", "Drink", 95),
    ],

    "Desserts": [
        ("Kunafa", "Dessert", 85),
        ("Molten Cake", "Dessert", 95),
        ("Rice Pudding", "Dessert", 65),
        ("Ice Cream", "Dessert", 55),
        ("Cheesecake", "Dessert", 95),
        ("Coffee", "Drink", 65),
    ],

    "Egyptian": [
        ("Koshary", "Main Course", 90),
        ("Hawawshi", "Main Course", 95),
        ("Grilled Kofta", "Main Course", 170),
        ("Mixed Grill", "Main Course", 260),
        ("Mahshi", "Main Course", 140),
        ("Molokhia", "Main Course", 90),
        ("Rice", "Side", 35),
    ],

    "Cafe": [
        ("Latte", "Coffee", 85),
        ("Cappuccino", "Coffee", 90),
        ("Espresso", "Coffee", 60),
        ("Mocha", "Coffee", 95),
        ("Cheesecake", "Dessert", 95),
        ("Croissant", "Bakery", 55),
    ],

    "Bakery": [
        ("Croissant", "Bakery", 55),
        ("Chocolate Donut", "Bakery", 45),
        ("Baguette", "Bakery", 35),
        ("Muffin", "Bakery", 55),
        ("Cinnamon Roll", "Bakery", 65),
    ]
}
menu_items = []
for _, restaurant in restaurants.iterrows():

    restaurant_name = restaurant["restaurant_name"]
    cuisine = restaurant["cuisine"]

    available_items = menu_templates[cuisine]

    number_of_items = random.randint(
        min(5, len(available_items)),
        len(available_items)
    )

    selected_items = random.sample(
        available_items,
        number_of_items
    )
    for item_name, category, base_price in selected_items:

        price = round(
            base_price * random.uniform(0.9, 1.1)
        )

        menu_items.append({

            "restaurant_name": restaurant_name,

            "cuisine": cuisine,

            "item_name": item_name,

            "category": category,

            "price": price

        })
menu_df = pd.DataFrame(menu_items)

output_path = BASE_DIR / "data" / "raw" / "restaurant_menu_seed.csv"

menu_df.to_csv(output_path, index=False)

print("Restaurant Menu Seed Generated Successfully")            