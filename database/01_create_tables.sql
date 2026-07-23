USE FoodDeliveryAnalytics;
GO

CREATE TABLE Customers(
    customer_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    gender NVARCHAR(10) NOT NULL,
    age INT NOT NULL,
    phone NVARCHAR(20) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    city NVARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE Restaurants(
    restaurant_id INT PRIMARY KEY,
    restaurant_name NVARCHAR(150) NOT NULL,
    cuisine NVARCHAR(100) NOT NULL,
    city NVARCHAR(50) NOT NULL,
    rating DECIMAL(3,1) NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL
);

CREATE TABLE Drivers(
    driver_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    gender NVARCHAR(10) NOT NULL,
    age INT NOT NULL,
    phone NVARCHAR(20) NOT NULL,
    city NVARCHAR(50) NOT NULL,
    vehicle_type NVARCHAR(30) NOT NULL,
    rating DECIMAL(3,1) NOT NULL,
    joining_date DATE NOT NULL,
    status NVARCHAR(20) NOT NULL
);

CREATE TABLE Menu_Items(
    item_id INT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    item_name NVARCHAR(150) NOT NULL,
    category NVARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE Orders(
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    driver_id INT NOT NULL,
    order_datetime DATETIME NOT NULL,
    delivery_datetime DATETIME NOT NULL,
    order_status NVARCHAR(30) NOT NULL,
    payment_method NVARCHAR(30) NOT NULL,
    delivery_fee DECIMAL(10,2) NOT NULL
);

CREATE TABLE Order_Items(
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE Payments(
    payment_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method NVARCHAR(30) NOT NULL,
    payment_status NVARCHAR(30) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_datetime DATETIME NOT NULL
);

CREATE TABLE Reviews(
    review_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    driver_id INT NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    review_text NVARCHAR(500),
    review_date DATE NOT NULL
);
GO
