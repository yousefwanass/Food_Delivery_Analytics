import pandas as pd
from pathlib import Path

# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parents[2]

restaurants_path = BASE_DIR / "data" / "raw" / "restaurants.csv"

menu_path = BASE_DIR / "data" / "raw" / "restaurant_menu_seed.csv"

output_path = BASE_DIR / "data" / "raw" / "menu_items.csv"

# ==========================
# Read Data
# ==========================

restaurants_df = pd.read_csv(restaurants_path)

menu_df = pd.read_csv(menu_path)

# ==========================
# Merge restaurant_id
# ==========================

merged = menu_df.merge(

    restaurants_df[["restaurant_id", "restaurant_name"]],

    on="restaurant_name",

    how="left"

)

# ==========================
# Create item_id
# ==========================

merged.insert(
    0,
    "item_id",
    range(1, len(merged) + 1)
)

# ترتيب الأعمدة

merged = merged[

    [

        "item_id",

        "restaurant_id",

        "item_name",

        "category",

        "price"

    ]

]

# ==========================
# Save
# ==========================

merged.to_csv(output_path, index=False)

print("Menu Items Generated Successfully")