--------------------------------------------------
-- 51. Top 10 Best Selling Menu Items
--------------------------------------------------

SELECT TOP 10

    m.item_name,

    SUM(oi.quantity) AS Total_Quantity_Sold

FROM Menu_Items m

JOIN Order_Items oi
ON m.item_id = oi.item_id

GROUP BY m.item_name

ORDER BY Total_Quantity_Sold DESC;


--------------------------------------------------
-- 52. Top 10 Menu Items By Revenue
--------------------------------------------------

SELECT TOP 10

    m.item_name,

    SUM(oi.quantity * oi.unit_price) AS Revenue

FROM Menu_Items m

JOIN Order_Items oi
ON m.item_id = oi.item_id

GROUP BY m.item_name

ORDER BY Revenue DESC;


--------------------------------------------------
-- 53. Revenue By Category
--------------------------------------------------

SELECT

    m.category,

    SUM(oi.quantity * oi.unit_price) AS Revenue

FROM Menu_Items m

JOIN Order_Items oi
ON m.item_id = oi.item_id

GROUP BY m.category

ORDER BY Revenue DESC;


--------------------------------------------------
-- 54. Average Item Price By Category
--------------------------------------------------

SELECT

    category,

    ROUND(AVG(price),2) AS Avg_Price

FROM Menu_Items

GROUP BY category

ORDER BY Avg_Price DESC;


--------------------------------------------------
-- 55. Most Expensive Menu Items
--------------------------------------------------

SELECT TOP 10

item_name,

category,

price

FROM Menu_Items

ORDER BY price DESC;


--------------------------------------------------
-- 56. Cheapest Menu Items
--------------------------------------------------

SELECT TOP 10

item_name,

category,

price

FROM Menu_Items

ORDER BY price ASC;


--------------------------------------------------
-- 57. Number Of Menu Items Per Restaurant
--------------------------------------------------

SELECT

    r.restaurant_name,

    COUNT(m.item_id) AS Total_Menu_Items

FROM Restaurants r

JOIN Menu_Items m
ON r.restaurant_id = m.restaurant_id

GROUP BY r.restaurant_name

ORDER BY Total_Menu_Items DESC;


--------------------------------------------------
-- 58. Average Menu Item Price Per Restaurant
--------------------------------------------------

SELECT

    r.restaurant_name,

    ROUND(AVG(m.price),2) AS Avg_Menu_Price

FROM Restaurants r

JOIN Menu_Items m
ON r.restaurant_id = m.restaurant_id

GROUP BY r.restaurant_name

ORDER BY Avg_Menu_Price DESC;


--------------------------------------------------
-- 59. Best Selling Category
--------------------------------------------------

SELECT

    m.category,

    SUM(oi.quantity) AS Total_Items_Sold

FROM Menu_Items m

JOIN Order_Items oi
ON m.item_id = oi.item_id

GROUP BY m.category

ORDER BY Total_Items_Sold DESC;


--------------------------------------------------
-- 60. Restaurant Menu Revenue
--------------------------------------------------

SELECT

    r.restaurant_name,

    SUM(oi.quantity * oi.unit_price) AS Revenue

FROM Restaurants r

JOIN Menu_Items m
ON r.restaurant_id = m.restaurant_id

JOIN Order_Items oi
ON m.item_id = oi.item_id

GROUP BY r.restaurant_name

ORDER BY Revenue DESC;