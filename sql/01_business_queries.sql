USE FoodDeliveryAnalytics;
GO

--------------------------------------------------
-- 1. Total Customers
--------------------------------------------------

SELECT COUNT(*) AS Total_Customers
FROM Customers;

--------------------------------------------------
-- 2. Total Restaurants
--------------------------------------------------

SELECT COUNT(*) AS Total_Restaurants
FROM Restaurants;

--------------------------------------------------
-- 3. Total Drivers
--------------------------------------------------

SELECT COUNT(*) AS Total_Drivers
FROM Drivers;

--------------------------------------------------
-- 4. Total Orders
--------------------------------------------------

SELECT COUNT(*) AS Total_Orders
FROM Orders;

--------------------------------------------------
-- 5. Orders By Status
--------------------------------------------------

SELECT
    order_status,
    COUNT(*) AS Total_Orders
FROM Orders
GROUP BY order_status
ORDER BY Total_Orders DESC;

--------------------------------------------------
-- 6. Orders By Payment Method
--------------------------------------------------

SELECT
    payment_method,
    COUNT(*) AS Total_Orders
FROM Orders
GROUP BY payment_method
ORDER BY Total_Orders DESC;

--------------------------------------------------
-- 7. Customers Per City
--------------------------------------------------

SELECT
    city,
    COUNT(*) AS Customers_Count
FROM Customers
GROUP BY city
ORDER BY Customers_Count DESC;

--------------------------------------------------
-- 8. Restaurants Per City
--------------------------------------------------

SELECT
    city,
    COUNT(*) AS Restaurants_Count
FROM Restaurants
GROUP BY city
ORDER BY Restaurants_Count DESC;

--------------------------------------------------
-- 9. Drivers By Status
--------------------------------------------------

SELECT
    status,
    COUNT(*) AS Drivers_Count
FROM Drivers
GROUP BY status;

--------------------------------------------------
-- 10. Average Restaurant Rating
--------------------------------------------------
