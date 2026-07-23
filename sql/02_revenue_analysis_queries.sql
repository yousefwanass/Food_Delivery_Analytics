--------------------------------------------------
-- 11. Total Revenue
--------------------------------------------------

SELECT
    SUM(amount_paid) AS Total_Revenue
FROM Payments
WHERE payment_status='Paid';

--------------------------------------------------
-- 12. Average Order Value
--------------------------------------------------

SELECT
    ROUND(AVG(amount_paid),2) AS Average_Order_Value
FROM Payments
WHERE payment_status='Paid';

--------------------------------------------------
-- 13. Revenue By Payment Method
--------------------------------------------------

SELECT
    payment_method,
    SUM(amount_paid) AS Revenue
FROM Payments
WHERE payment_status='Paid'
GROUP BY payment_method
ORDER BY Revenue DESC;

--------------------------------------------------
-- 14. Monthly Revenue
--------------------------------------------------

SELECT
    YEAR(payment_datetime) AS Year,
    MONTH(payment_datetime) AS Month,
    SUM(amount_paid) AS Revenue
FROM Payments
WHERE payment_status='Paid'
GROUP BY YEAR(payment_datetime),MONTH(payment_datetime)
ORDER BY Year,Month;

--------------------------------------------------
-- 15. Daily Revenue
--------------------------------------------------

SELECT
    CAST(payment_datetime AS DATE) AS Payment_Date,
    SUM(amount_paid) AS Revenue
FROM Payments
WHERE payment_status='Paid'
GROUP BY CAST(payment_datetime AS DATE)
ORDER BY Payment_Date;

--------------------------------------------------
-- 16. Top 10 Restaurants By Revenue
--------------------------------------------------

SELECT TOP 10

    r.restaurant_name,

    SUM(oi.quantity*oi.unit_price) AS Revenue

FROM Orders o

JOIN Restaurants r
ON o.restaurant_id=r.restaurant_id

JOIN Order_Items oi
ON o.order_id=oi.order_id

GROUP BY r.restaurant_name

ORDER BY Revenue DESC;

--------------------------------------------------
-- 17. Revenue By City
--------------------------------------------------

SELECT

    r.city,

    SUM(oi.quantity*oi.unit_price) AS Revenue

FROM Orders o

JOIN Restaurants r
ON o.restaurant_id=r.restaurant_id

JOIN Order_Items oi
ON o.order_id=oi.order_id

GROUP BY r.city

ORDER BY Revenue DESC;

--------------------------------------------------
-- 18. Highest Delivery Fees
--------------------------------------------------

SELECT TOP 10

order_id,

delivery_fee

FROM Orders

ORDER BY delivery_fee DESC;

--------------------------------------------------
-- 19. Average Delivery Fee
--------------------------------------------------

SELECT

ROUND(AVG(delivery_fee),2) AS Avg_Delivery_Fee

FROM Orders;

--------------------------------------------------
-- 20. Total Delivery Fees
--------------------------------------------------

SELECT

SUM(delivery_fee) AS Total_Delivery_Fees

FROM Orders;