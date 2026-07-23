--------------------------------------------------
-- 41. Top 10 Drivers By Number of Deliveries
--------------------------------------------------

SELECT TOP 10

    d.driver_id,
    d.first_name + ' ' + d.last_name AS Driver_Name,
    COUNT(o.order_id) AS Total_Deliveries

FROM Drivers d

JOIN Orders o
ON d.driver_id = o.driver_id

GROUP BY
    d.driver_id,
    d.first_name,
    d.last_name

ORDER BY Total_Deliveries DESC;


--------------------------------------------------
-- 42. Top 10 Drivers By Revenue Delivered
--------------------------------------------------

SELECT TOP 10

    d.driver_id,
    d.first_name + ' ' + d.last_name AS Driver_Name,
    SUM(p.amount_paid) AS Revenue

FROM Drivers d

JOIN Orders o
ON d.driver_id = o.driver_id

JOIN Payments p
ON o.order_id = p.order_id

WHERE p.payment_status='Paid'

GROUP BY
    d.driver_id,
    d.first_name,
    d.last_name

ORDER BY Revenue DESC;


--------------------------------------------------
-- 43. Average Driver Rating
--------------------------------------------------

SELECT

ROUND(AVG(rating),2) AS Average_Driver_Rating

FROM Drivers;


--------------------------------------------------
-- 44. Highest Rated Drivers
--------------------------------------------------

SELECT

driver_id,

first_name + ' ' + last_name AS Driver_Name,

rating

FROM Drivers

ORDER BY rating DESC;


--------------------------------------------------
-- 45. Drivers By Status
--------------------------------------------------

SELECT

status,

COUNT(*) AS Total_Drivers

FROM Drivers

GROUP BY status

ORDER BY Total_Drivers DESC;


--------------------------------------------------
-- 46. Drivers By Vehicle Type
--------------------------------------------------

SELECT

vehicle_type,

COUNT(*) AS Total_Drivers

FROM Drivers

GROUP BY vehicle_type

ORDER BY Total_Drivers DESC;


--------------------------------------------------
-- 47. Average Delivery Time (Minutes)
--------------------------------------------------

SELECT

ROUND(
AVG(
DATEDIFF(
MINUTE,
order_datetime,
delivery_datetime
)
),2) AS Avg_Delivery_Time_Minutes

FROM Orders;


--------------------------------------------------
-- 48. Fastest Deliveries
--------------------------------------------------

SELECT TOP 10

order_id,

DATEDIFF(
MINUTE,
order_datetime,
delivery_datetime
) AS Delivery_Time_Minutes

FROM Orders

ORDER BY Delivery_Time_Minutes ASC;


--------------------------------------------------
-- 49. Slowest Deliveries
--------------------------------------------------

SELECT TOP 10

order_id,

DATEDIFF(
MINUTE,
order_datetime,
delivery_datetime
) AS Delivery_Time_Minutes

FROM Orders

ORDER BY Delivery_Time_Minutes DESC;


--------------------------------------------------
-- 50. Driver Performance Summary
--------------------------------------------------

SELECT

    d.driver_id,

    d.first_name + ' ' + d.last_name AS Driver_Name,

    d.rating,

    COUNT(o.order_id) AS Total_Deliveries,

    ROUND(
        AVG(
            DATEDIFF(
                MINUTE,
                o.order_datetime,
                o.delivery_datetime
            )
        ),2
    ) AS Avg_Delivery_Time

FROM Drivers d

LEFT JOIN Orders o
ON d.driver_id = o.driver_id

GROUP BY

    d.driver_id,

    d.first_name,

    d.last_name,

    d.rating

ORDER BY Total_Deliveries DESC;