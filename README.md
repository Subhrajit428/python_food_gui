# Food Delivery Management System

## Project Overview

The **Food Delivery Management System** is a desktop-based application developed using Python's Tkinter library and SQLite database. It provides a simple graphical user interface to manage customers, food menu items, customer orders, and order history.

The application helps simplify food delivery operations by allowing users to manage customer information, maintain a food menu, place orders, calculate bills automatically, and track order status.

## Technologies Used

- **Python:** Core programming language.
- **Tkinter:** Used to develop the graphical user interface (GUI).
- **SQLite3:** Used for database management and data storage.
- **ttk:** Used for enhanced GUI widgets.
- **Datetime:** Used to record order dates and times.

## Features

### 1. Customer Management
- Add new customers.
- Store customer name, phone number, and address.
- View customer records.
- Delete customer records when they have no associated orders.

### 2. Food Menu Management
- Add new food items.
- Specify food category and price.
- View all available food items.
- Update food availability.
- Delete food items that are not associated with previous orders.

### 3. Order Management
- Select customers from the registered customer list.
- Browse available food items.
- Add multiple food items to an order.
- Specify item quantities.
- Automatically calculate the total bill.
- Place and save customer orders.

### 4. Order History
- View all previously placed orders.
- View customer details and order information.
- Check individual order items.
- Update order status.

### 5. Order Status Tracking

Orders can have the following statuses:
- Pending
- Preparing
- Out for Delivery
- Delivered
- Cancelled

## Project Structure

```text
python_food_gui/
│
├── food.py
│
├── food_delivery.db
│
├── README.md
│
└── .gitignore
```

**Note:** The SQLite database file is automatically generated when the application runs for the first time.

## Database Design

The project uses SQLite with four main tables:

| Table Name | Description |
|---|---|
| customers | Stores customer information |
| menu_items | Stores food items, categories, and prices |
| orders | Stores customer orders and their status |
| order_items | Stores individual food items associated with orders |

### Database Relationships

- One customer can place multiple orders.
- One order can contain multiple food items.
- Each order item is associated with a menu item.
- Foreign keys maintain relationships between the tables.

## Installation and Execution

### Prerequisites

- Python 3.x
- Any Python IDE (VS Code, PyCharm, IDLE, etc.)

Tkinter and SQLite3 are included with most standard Python installations.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Subhrajit428/python_food_gui.git
```

### Step 2: Navigate to the Project Folder

```bash
cd python_food_gui
```

### Step 3: Run the Application

```bash
python food.py
```

### Step 4: Start Using the Application

The application window will open, and the SQLite database will be created automatically.

## Sample Food Items

The application initially provides the following sample menu items:

| Food Item | Category | Price |
|---|---|---:|
| Veg Burger | Fast Food | ₹90 |
| Cheese Pizza | Fast Food | ₹220 |
| Paneer Roll | Indian | ₹130 |
| Veg Biryani | Indian | ₹160 |
| Masala Dosa | South Indian | ₹100 |
| Cold Coffee | Beverage | ₹80 |
| Chocolate Brownie | Dessert | ₹110 |

## Advantages

- Simple and user-friendly graphical interface.
- Automatic bill calculation.
- Persistent data storage using SQLite.
- Easy customer and menu management.
- Efficient order tracking.
- No external database server required.

## Future Enhancements

- Admin login and authentication.
- Online payment integration.
- Delivery person management.
- Real-time delivery tracking.
- Order cancellation and refund management.
- Sales reports and analytics.
- Search and filter functionality.
- Customer feedback and ratings.

## Conclusion

The Food Delivery Management System demonstrates the practical implementation of Python GUI development and database connectivity. It provides an organized way to manage customers, food items, and orders while demonstrating important programming concepts such as CRUD operations, SQL queries, database relationships, and event-driven programming.

## Author

**Developed as a Python and Database Management System (DBMS) project.**