# Beach-View Hotel Management System

## Overview
The Beach-View Hotel Management System is a web-based application that allows users to search for hotel rooms, view availability, check prices, and manage bookings. The system supports two types of users: customers and administrators. Customers can browse room options, book rooms, and manage reservations. Administrators can update hotel details and manage customer reservations.

This project was developed as part of a **Database Management Systems (DBMS)** course using **HTML**, **CSS**, **Django** for the backend, and **MySQL** for the database.

## Features
- **Room Booking:** Customers can book available rooms based on the type and availability.
- **Room Availability:** Users can check the availability of rooms for a specific date.
- **Price Details:** View pricing for different room categories such as Economy, Deluxe, Deluxe Plus, and Suite.
- **Booking Management:** Customers can view and cancel their bookings.
- **Admin Dashboard:** Manage room bookings, update availability, and modify customer details.

## Technologies Used
- **Frontend:** HTML, CSS
- **Backend:** Django (Python)
- **Database:** MySQL
- **Development Environment:** PyCharm
- **Web Server:** Apache (via XAMPP)

## System Requirements
- **Software:**
  - Python 3.x
  - Django 4.x
  - MySQL 8.x
  - XAMPP for MySQL and Apache
  - PyCharm (optional, but recommended)

- **Hardware:**
  - Minimum 4GB RAM
  - Internet connection for Django server and MySQL

## Database Schema
The system uses several MySQL tables, including:
- `room_class`: Stores room categories and their prices.
- `room_info`: Stores details about individual rooms and their availability.
- `cust_info`: Stores customer information.
- `reservation`: Stores reservation details linking customers to rooms.

### Example Queries:
- Create `room_class` table:
  ```sql
  CREATE TABLE room_class (
    class_ID INT NOT NULL PRIMARY KEY,
    name VARCHAR(15),
    price INT
  );
- Insert room class data:
  ```sql
  INSERT INTO room_class VALUES (1, 'Economy', 1699), (2, 'Deluxe', 3145), (3, 'Deluxe Plus', 4499), (4, 'Suite', 7299);
- Create reservation table:
  ```sql
  CREATE TABLE reservation (
    reservation_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    room_id INT,
    res_date DATETIME,
    check_in DATE,
    check_out DATE,
    FOREIGN KEY (cust_id) REFERENCES cust_info(cust_id),
    FOREIGN KEY (room_id) REFERENCES room_info(room_id)
  );
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/username/hotel-management-system.git
    ```

2. Navigate to the project directory:
    ```bash
    cd hotel-management-system
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the MySQL database using the provided schema.

5. Start the Django server:
    ```bash
    python manage.py runserver
    ```

6. Access the application at [http://localhost:8000](http://localhost:8000).

## Usage

### For Customers:
- Navigate to the home page.
- Check room availability by selecting a date.
- View prices of different room categories.
- Sign up or log in to book a room.
- Manage your reservations by viewing and canceling them.

### For Administrators:
- Log in to access the admin dashboard.
- Add or update room information.
- View and manage customer reservations.

## Future Enhancements
- Add a payment gateway for online transactions.
- Include booking cancellation for more flexibility.
- Implement real-time notifications for booking confirmations.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Commit your changes:
    ```bash
    git commit -am 'Add new feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
