USE FoodDeliveryAnalytics;
GO

ALTER TABLE Menu_Items
ADD CONSTRAINT FK_MenuItems_Restaurants
FOREIGN KEY (restaurant_id)
REFERENCES Restaurants(restaurant_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Orders_Customers
FOREIGN KEY (customer_id)
REFERENCES Customers(customer_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Orders_Restaurants
FOREIGN KEY (restaurant_id)
REFERENCES Restaurants(restaurant_id);

ALTER TABLE Orders
ADD CONSTRAINT FK_Orders_Drivers
FOREIGN KEY (driver_id)
REFERENCES Drivers(driver_id);

ALTER TABLE Order_Items
ADD CONSTRAINT FK_OrderItems_Orders
FOREIGN KEY (order_id)
REFERENCES Orders(order_id);

ALTER TABLE Order_Items
ADD CONSTRAINT FK_OrderItems_MenuItems
FOREIGN KEY (item_id)
REFERENCES Menu_Items(item_id);

ALTER TABLE Payments
ADD CONSTRAINT FK_Payments_Orders
FOREIGN KEY (order_id)
REFERENCES Orders(order_id);

ALTER TABLE Reviews
ADD CONSTRAINT FK_Reviews_Orders
FOREIGN KEY (order_id)
REFERENCES Orders(order_id);

ALTER TABLE Reviews
ADD CONSTRAINT FK_Reviews_Customers
FOREIGN KEY (customer_id)
REFERENCES Customers(customer_id);

ALTER TABLE Reviews
ADD CONSTRAINT FK_Reviews_Restaurants
FOREIGN KEY (restaurant_id)
REFERENCES Restaurants(restaurant_id);

ALTER TABLE Reviews
ADD CONSTRAINT FK_Reviews_Drivers
FOREIGN KEY (driver_id)
REFERENCES Drivers(driver_id);
GO
