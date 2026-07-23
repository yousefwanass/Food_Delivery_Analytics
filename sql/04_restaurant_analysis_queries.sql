--------------------------------------------------
-- 31. Top 10 Restaurants By Number of Orders
--------------------------------------------------

SELECT TOP 10

    r.restaurant_name,
    COUNT(o.order_id) AS Total_Orders

FROM Restaurants r

JOIN Orders o
ON r.restaurant_id = o.restaurant_id

GROUP BY r.restaurant_name

ORDER BY Total_Orders DESC;


--------------------------------------------------
-- 32. Top 10 Restaurants By Revenue
--------------------------------------------------

SELECT TOP 10

    r.restaurant_name,

    SUM(oi.quantity * oi.unit_price) AS Revenue

FROM Restaurants r

JOIN Orders o
ON r.restaurant_id = o.restaurant_id

JOIN Order_Items oi
ON o.order_id = oi.order_id

GROUP BY r.restaurant_name

ORDER BY Revenue DESC;


--------------------------------------------------
-- 33. Average Order Value Per Restaurant
--------------------------------------------------

SELECT

    r.restaurant_name,

    ROUND(AVG(Order_Total),2) AS Average_Order_Value

FROM
(
    SELECT

        o.order_id,
        o.restaurant_id,

        SUM(oi.quantity * oi.unit_price) AS Order_Total

    FROM Orders o

    JOIN Order_Items oi
    ON o.order_id = oi.order_id

    GROUP BY
        o.order_id,
        o.restaurant_id

) x

JOIN Restaurants r
ON x.restaurant_id = r.restaurant_id

GROUP BY r.restaurant_name

ORDER BY Average_Order_Value DESC;


--------------------------------------------------
-- 34. Highest Rated Restaurants
--------------------------------------------------

SELECT

restaurant_name,

rating

FROM Restaurants

ORDER BY rating DESC;


--------------------------------------------------
-- 35. Restaurants By Cuisine
--------------------------------------------------

SELECT

cuisine,

COUNT(*) AS Total_Restaurants

FROM Restaurants

GROUP BY cuisine

ORDER BY Total_Restaurants DESC;


--------------------------------------------------
-- 36. Average Rating By Cuisine
--------------------------------------------------

SELECT

cuisine,

ROUND(AVG(rating),2) AS Average_Rating

FROM Restaurants

GROUP BY cuisine

ORDER BY Average_Rating DESC;


--------------------------------------------------
-- 37. Restaurants By City
--------------------------------------------------

SELECT

city,

COUNT(*) AS Total_Restaurants

FROM Restaurants

GROUP BY city

ORDER BY Total_Restaurants DESC;


--------------------------------------------------
-- 38. Revenue By Cuisine
--------------------------------------------------

SELECT

    r.cuisine,

    SUM(oi.quantity * oi.unit_price) AS Revenue

FROM Restaurants r

JOIN Orders o
ON r.restaurant_id = o.restaurant_id

JOIN Order_Items oi
ON o.order_id = oi.order_id

GROUP BY r.cuisine

ORDER BY Revenue DESC;


--------------------------------------------------
-- 39. Most Popular Restaurant In Each City
--------------------------------------------------

WITH RestaurantOrders AS
(
    SELECT

        r.city,
        r.restaurant_name,
        COUNT(o.order_id) AS Total_Orders,

        ROW_NUMBER() OVER
        (
            PARTITION BY r.city
            ORDER BY COUNT(o.order_id) DESC
        ) AS rn

    FROM Restaurants r

    JOIN Orders o
    ON r.restaurant_id = o.restaurant_id

    GROUP BY
        r.city,
        r.restaurant_name
)

SELECT

city,
restaurant_name,
Total_Orders

FROM RestaurantOrders

WHERE rn = 1;


--------------------------------------------------
-- 40. Restaurant Performance Summary
--------------------------------------------------

SELECT

    r.restaurant_name,

    COUNT(DISTINCT o.order_id) AS Orders_Count,

    SUM(oi.quantity * oi.unit_price) AS Revenue,

    ROUND(AVG(r.rating),2) AS Rating

FROM Restaurants r

LEFT JOIN Orders o
ON r.restaurant_id = o.restaurant_id

LEFT JOIN Order_Items oi
ON o.order_id = oi.order_id

GROUP BY
    r.restaurant_name

ORDER BY Revenue DESC;