import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=FoodDeliveryAnalytics;"
    "Trusted_Connection=yes;"
)

customers = pd.read_sql("SELECT * FROM Customers", conn)
restaurants = pd.read_sql("SELECT * FROM Restaurants", conn)
drivers = pd.read_sql("SELECT * FROM Drivers", conn)
orders = pd.read_sql("SELECT * FROM Orders", conn)
payments = pd.read_sql("SELECT * FROM Payments", conn)

# ================= KPI =================

kpi = pd.DataFrame({
    "Metric":[
        "Total Customers",
        "Total Restaurants",
        "Total Drivers",
        "Total Orders",
        "Total Revenue",
        "Average Order Value"
    ],
    "Value":[
        len(customers),
        len(restaurants),
        len(drivers),
        len(orders),
        payments["amount_paid"].sum(),
        round(payments["amount_paid"].mean(),2)
    ]
})

# Revenue By Payment Method
revenue_payment = (
    payments.groupby("payment_method")["amount_paid"]
    .sum()
    .reset_index()
)

# Orders By Status
orders_status = (
    orders.groupby("order_status")
    .size()
    .reset_index(name="Orders")
)

# Customers By City
customers_city = (
    customers.groupby("city")
    .size()
    .reset_index(name="Customers")
)

# Customers By Gender
customers_gender = (
    customers.groupby("gender")
    .size()
    .reset_index(name="Customers")
)

# Top Customers
top_customers = (
    orders.groupby("customer_id")
    .size()
    .reset_index(name="Orders")
    .sort_values("Orders",ascending=False)
    .head(20)
)

# Top Restaurants
top_restaurants = (
    orders.groupby("restaurant_id")
    .size()
    .reset_index(name="Orders")
    .sort_values("Orders",ascending=False)
    .head(20)
)

# Top Drivers
top_drivers = (
    orders.groupby("driver_id")
    .size()
    .reset_index(name="Deliveries")
    .sort_values("Deliveries",ascending=False)
    .head(20)
)

# Monthly Revenue
payments["payment_datetime"] = pd.to_datetime(payments["payment_datetime"])

monthly_revenue = (
    payments.groupby(payments["payment_datetime"].dt.to_period("M"))["amount_paid"]
    .sum()
    .reset_index()
)

monthly_revenue["payment_datetime"] = monthly_revenue["payment_datetime"].astype(str)

# ================= Export =================

with pd.ExcelWriter("analysis_results.xlsx") as writer:

    kpi.to_excel(writer,sheet_name="KPIs",index=False)
    revenue_payment.to_excel(writer,sheet_name="Revenue",index=False)
    orders_status.to_excel(writer,sheet_name="Orders Status",index=False)
    customers_city.to_excel(writer,sheet_name="Customers City",index=False)
    customers_gender.to_excel(writer,sheet_name="Customers Gender",index=False)
    top_customers.to_excel(writer,sheet_name="Top Customers",index=False)
    top_restaurants.to_excel(writer,sheet_name="Top Restaurants",index=False)
    top_drivers.to_excel(writer,sheet_name="Top Drivers",index=False)
    monthly_revenue.to_excel(writer,sheet_name="Monthly Revenue",index=False)

print("analysis_results.xlsx created successfully!")

conn.close()