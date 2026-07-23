--------------------------------------------------
-- 21. Top 10 Customers By Number of Orders
--------------------------------------------------

SELECT TOP 10

    c.customer_id,
    c.first_name + ' ' + c.last_name AS Customer_Name,
    COUNT(o.order_id) AS Total_Orders

FROM Customers c

JOIN Orders o
ON c.customer_id = o.customer_id

GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name

ORDER BY Total_Orders DESC;


--------------------------------------------------
-- 22. Top 10 Customers By Total Spending
--------------------------------------------------

SELECT TOP 10

    c.customer_id,
    c.first_name + ' ' + c.last_name AS Customer_Name,
    SUM(p.amount_paid) AS Total_Spending

FROM Customers c

JOIN Orders o
ON c.customer_id = o.customer_id

JOIN Payments p
ON o.order_id = p.order_id

WHERE p.payment_status = 'Paid'

GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name

ORDER BY Total_Spending DESC;


--------------------------------------------------
-- 23. Average Customer Spending
--------------------------------------------------

SELECT

ROUND(AVG(Customer_Total),2) AS Avg_Customer_Spending

FROM
(
    SELECT

        c.customer_id,

        SUM(p.amount_paid) AS Customer_Total

    FROM Customers c

    JOIN Orders o
    ON c.customer_id=o.customer_id

    JOIN Payments p
    ON o.order_id=p.order_id

    WHERE p.payment_status='Paid'

    GROUP BY c.customer_id

) t;


--------------------------------------------------
-- 24. Customers By Gender
--------------------------------------------------

SELECT

gender,

COUNT(*) AS Total_Customers

FROM Customers

GROUP BY gender;


--------------------------------------------------
-- 25. Customers By Age Group
--------------------------------------------------

SELECT

CASE

WHEN age BETWEEN 18 AND 25 THEN '18-25'
WHEN age BETWEEN 26 AND 35 THEN '26-35'
WHEN age BETWEEN 36 AND 45 THEN '36-45'
ELSE '46+'

END AS Age_Group,

COUNT(*) AS Total_Customers

FROM Customers

GROUP BY

CASE

WHEN age BETWEEN 18 AND 25 THEN '18-25'
WHEN age BETWEEN 26 AND 35 THEN '26-35'
WHEN age BETWEEN 36 AND 45 THEN '36-45'
ELSE '46+'

END

ORDER BY Age_Group;


--------------------------------------------------
-- 26. New Customers Per Month
--------------------------------------------------

SELECT

YEAR(signup_date) AS Year,

MONTH(signup_date) AS Month,

COUNT(*) AS New_Customers

FROM Customers

GROUP BY

YEAR(signup_date),

MONTH(signup_date)

ORDER BY Year,Month;


--------------------------------------------------
-- 27. Customers Per City
--------------------------------------------------

SELECT

city,

COUNT(*) AS Customers_Count

FROM Customers

GROUP BY city

ORDER BY Customers_Count DESC;


--------------------------------------------------
-- 28. Customers With No Orders
--------------------------------------------------

SELECT

c.customer_id,

c.first_name,

c.last_name

FROM Customers c

LEFT JOIN Orders o

ON c.customer_id=o.customer_id

WHERE o.order_id IS NULL;


--------------------------------------------------
-- 29. Customers With More Than 10 Orders
--------------------------------------------------

SELECT

c.customer_id,

c.first_name + ' ' + c.last_name AS Customer_Name,

COUNT(o.order_id) AS Orders_Count

FROM Customers c

JOIN Orders o

ON c.customer_id=o.customer_id

GROUP BY

c.customer_id,

c.first_name,

c.last_name

HAVING COUNT(o.order_id)>10

ORDER BY Orders_Count DESC;


--------------------------------------------------
-- 30. Customer Lifetime Value (CLV)
--------------------------------------------------

SELECT

c.customer_id,

c.first_name + ' ' + c.last_name AS Customer_Name,

SUM(p.amount_paid) AS Customer_Lifetime_Value

FROM Customers c

JOIN Orders o
ON c.customer_id=o.customer_id

JOIN Payments p
ON o.order_id=p.order_id

WHERE p.payment_status='Paid'

GROUP BY

c.customer_id,

c.first_name,

c.last_name

ORDER BY Customer_Lifetime_Value DESC;