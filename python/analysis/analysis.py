import pandas as pd
import pyodbc

# ==========================
# SQL Connection
# ==========================

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=FoodDeliveryAnalytics;"
    "Trusted_Connection=yes;"
)

print("Connected Successfully")

# ==========================
# Load Tables
# ==========================

customers = pd.read_sql("SELECT * FROM Customers", conn)

restaurants = pd.read_sql("SELECT * FROM Restaurants", conn)

drivers = pd.read_sql("SELECT * FROM Drivers", conn)

orders = pd.read_sql("SELECT * FROM Orders", conn)

order_items = pd.read_sql("SELECT * FROM Order_Items", conn)

payments = pd.read_sql("SELECT * FROM Payments", conn)

reviews = pd.read_sql("SELECT * FROM Reviews", conn)

menu_items = pd.read_sql("SELECT * FROM Menu_Items", conn)

print("All Tables Loaded")

# ==========================
# Basic Information
# ==========================

print("\nCustomers Shape:", customers.shape)

print("Restaurants Shape:", restaurants.shape)

print("Drivers Shape:", drivers.shape)

print("Orders Shape:", orders.shape)

print("Payments Shape:", payments.shape)

# ==========================
# Missing Values
# ==========================

print("\nMissing Values")

for name, df in {
    "Customers": customers,
    "Restaurants": restaurants,
    "Drivers": drivers,
    "Orders": orders,
    "Order_Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Menu_Items": menu_items
}.items():

    print(f"\n{name}")

    print(df.isnull().sum())

# ==========================
# Duplicate Rows
# ==========================

print("\nDuplicate Rows")

for name, df in {
    "Customers": customers,
    "Restaurants": restaurants,
    "Drivers": drivers,
    "Orders": orders,
    "Order_Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Menu_Items": menu_items
}.items():

    print(name, ":", df.duplicated().sum())

# ==========================
# KPIs
# ==========================

print("\n========== KPIs ==========")

print("Total Customers :", len(customers))

print("Total Restaurants :", len(restaurants))

print("Total Drivers :", len(drivers))

print("Total Orders :", len(orders))

print("Total Revenue :", round(payments["amount_paid"].sum(),2))

print("Average Order Value :", round(payments["amount_paid"].mean(),2))

print("Average Restaurant Rating :", round(restaurants["rating"].mean(),2))

print("Average Driver Rating :", round(drivers["rating"].mean(),2))

# ==========================
# Revenue by Payment Method
# ==========================

revenue_by_payment = (
    payments.groupby("payment_method")["amount_paid"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue By Payment Method")
print(revenue_by_payment)


# ==========================
# Orders by Status
# ==========================

orders_status = (
    orders["order_status"]
    .value_counts()
)

print("\nOrders By Status")
print(orders_status)


# ==========================
# Top 10 Customers
# ==========================

top_customers = (
    orders.groupby("customer_id")
    .size()
    .reset_index(name="total_orders")
    .sort_values("total_orders", ascending=False)
    .head(10)
)

print("\nTop 10 Customers")
print(top_customers)


# ==========================
# Top 10 Restaurants
# ==========================

top_restaurants = (
    orders.groupby("restaurant_id")
    .size()
    .reset_index(name="total_orders")
    .sort_values("total_orders", ascending=False)
    .head(10)
)

print("\nTop 10 Restaurants")
print(top_restaurants)


# ==========================
# Top 10 Drivers
# ==========================

top_drivers = (
    orders.groupby("driver_id")
    .size()
    .reset_index(name="total_orders")
    .sort_values("total_orders", ascending=False)
    .head(10)
)

print("\nTop 10 Drivers")
print(top_drivers)


# ==========================
# Orders by City
# ==========================

orders_city = (
    orders.merge(
        customers[["customer_id", "city"]],
        on="customer_id"
    )
)

orders_city = (
    orders_city.groupby("city")
    .size()
    .sort_values(ascending=False)
)

print("\nOrders By City")
print(orders_city)
conn.close()
