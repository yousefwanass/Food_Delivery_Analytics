USE FoodDeliveryAnalytics;
GO

CREATE INDEX IX_Customers_City ON Customers(city);

CREATE INDEX IX_Restaurants_City
ON Restaurants(city);

CREATE INDEX IX_MenuItems_Restaurant
ON Menu_Items(restaurant_id);

CREATE INDEX IX_Orders_Customer
ON Orders(customer_id);

CREATE INDEX IX_Orders_Restaurant
ON Orders(restaurant_id);

CREATE INDEX IX_Orders_Driver
ON Orders(driver_id);

CREATE INDEX IX_Orders_Date
ON Orders(order_datetime);

CREATE INDEX IX_OrderItems_Order
ON Order_Items(order_id);

CREATE INDEX IX_OrderItems_Item
ON Order_Items(item_id);

CREATE INDEX IX_Payments_Order
ON Payments(order_id);

CREATE INDEX IX_Reviews_Restaurant
ON Reviews(restaurant_id);

CREATE INDEX IX_Reviews_Driver
ON Reviews(driver_id);
GO
