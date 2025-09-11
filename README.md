# 🍽️ Restaurant Backend
---


## Overview
This project is built with **Python (Django REST Framework)** and **MySQL**, providing the API and business logic that powers restaurant operations. It is designed to make day-to-day workflow easier and more efficient for employees and managers, while keeping the system secure and organized.

---

 ## 👨‍🍳 Core Functionality
 
- **Menu Access** – The restaurant’s menu is publicly visible to all visitors.
- **Order Management** – Authenticated employees and managers can create and update orders for specific tables.
- **Billing Workflow** – When a table is ready to settle the bill, the order can be marked as completed, automatically freeing that table for new orders.

---

 ## 🔑 Role-Based Access

- **Employees**

    - View the menu.
    - Take and register orders for tables.

- **Managers**

    - Manage the menu (add, edit, or delete items).
    - Manage users (add, edit, or delete employees).
    - Access the completed orders log (orders grouped by table and timestamp) for auditing purposes.

---

## 🛠️ Tech Stack

- **Django** – High-level Python web framework used for building backend logic, models, and routing.
- **Django REST Framework (DRF)** – Adds REST API functionality to Django.  
- **Django REST Framework SimpleJWT** – Provides secure JWT-based authentication.  
- **MySQL + mysqlclient** – Relational database and Python connector.  
- **django-cors-headers** – Enables CORS for frontend-backend communication.  
- **python-dotenv** – Environment variables.

---

## 🚀 Backend Setup (Django + MySQL)

 1. **Clone the Repository**
    ```bash
    git clone https://github.com/chriskampolis/cf7-restaurant-backend.git
    cd cf7-restaurant-backend
    ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux/macOS
   venv\Scripts\activate        # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   copy .env.example .env   # use copy if cp is not working
   # Edit .env with SECRET_KEY and database settings
   ```
   
   Generate a new secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   # Paste the output into .env as SECRET_KEY=your-generated-key
   ```

   Variables to be filled for the .env file: 
   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key

   ALLOWED_HOSTS=127.0.0.1

   DB_NAME=db_name
   DB_USER=db_user
   DB_PASSWORD=db_password
   DB_HOST=localhost
   DB_PORT=3306

   CORS_ALLOW_CREDENTIALS=True
   CORS_ALLOWED_ORIGINS=http://localhost:5173
   ```

5. **Create the MySQL Database**
   ```sql
   CREATE SCHEMA `restaurant_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
   ```

6. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
   New users are auto-set as employees, to make the superuser a manager (adjust db_name if necessary):
   ```sql
   UPDATE `restaurant_db`.`restaurant_user` SET `role` = 'manager' WHERE (`id` = '1');
   ```

8. **Create Menu**
   ```sql
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (1,'Greek Salad',7.50,14,'APPETIZER');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (2,'Fava beans with caper leaves',6.00,8,'APPETIZER');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (3,'Grilled sardines',7.00,8,'APPETIZER');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (4,'Mussels with white wine',8.50,7,'APPETIZER');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (5,'Seafood risotto',12.50,8,'MAIN');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (6,'Sea bass with vegetables',15.00,9,'MAIN');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (7,'Shrimp pasta',13.50,7,'MAIN');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (8,'Melon sorbet',5.00,7,'DESSERT');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (9,'Seasonal fruit salad',7.00,10,'DESSERT');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (10,'Mineral water',1.50,23,'DRINK');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (11,'Souroti',3.00,13,'DRINK');
   INSERT INTO restaurant_db.restaurant_menuitem (`id`,`name`,`price`,`availability`,`category`) VALUES (12,'Mamos beer',4.00,18,'DRINK');
   ```
   Items on the menu can be inserted into the database - example values above (adjust db_name if necessary). Or they can be created by a manager from the UI's Menu Items page. 

9. **Run the Application**
   ```bash
   python manage.py runserver
   ```
The API will be available at:
👉 http://127.0.0.1:8000/

---

## 📌 Future Development
- `forms.py` and `admin.py` are reserved for future development (ex: better management interface / custom forms).
- Additional roles for users with different permissions (ex: customer / head-chef).
- Booking reservations: logged-in customers able to book tables.
- Menu filtering - Allow users to filter menu items by category (ex: appetizers only), improving navigation for large menus.