import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

orders = pd.read_csv(BASE_DIR / "data" / "raw" / "orders.csv")
order_items = pd.read_csv(BASE_DIR / "data" / "raw" / "order_items.csv")

payments = []

payment_id = 1

for _, order in orders.iterrows():

    items = order_items[
        order_items["order_id"] == order["order_id"]
    ]

    total = (
        items["quantity"] * items["unit_price"]
    ).sum()

    total += order["delivery_fee"]

    payment_status = "Paid"

    if order["order_status"] == "Cancelled":
        payment_status = "Refunded"

    elif order["order_status"] == "Failed":
        payment_status = "Failed"

    payments.append({

        "payment_id": payment_id,

        "order_id": order["order_id"],

        "payment_method": order["payment_method"],

        "payment_status": payment_status,

        "amount_paid": round(total,2),

        "payment_datetime": order["order_datetime"]

    })

    payment_id += 1

payments_df = pd.DataFrame(payments)

payments_df.to_csv(
    BASE_DIR / "data" / "raw" / "payments.csv",
    index=False
)

print("Payments Generated Successfully")