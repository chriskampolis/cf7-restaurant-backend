# 🍽️ Restaurant Backend
---

## Overview
---

This project is built with **Python (Django REST Framework)** and **MySQL**, providing the API and business logic that powers restaurant operations. It is designed to make day-to-day workflow easier and more efficient for employees and managers, while keeping the system secure and organized.

 ## 👨‍🍳 Core Functionality
 ---
- **Menu Access** – The restaurant’s menu is publicly visible to all visitors.
- **Order Management** – Authenticated employees and managers can create and update orders for specific tables.
- **Billing Workflow** – When a table requests the bill from a waiter, the order can be marked as completed, automatically freeing that table for new orders.

 ## 🔑 Role-Based Access
 ---
- **Employees**

    - View the menu.

    - Take and register orders for tables.

- **Managers**

    - Manage the menu (add, edit, or delete items).

    - Manage users (add, edit, or delete employees).

    - Access the completed orders log (orders grouped by table and timestamp) for auditing purposes.

---

## 🛠️ Tech Stack
---

- **Django** – High-level Python web framework used for building backend logic, models, and routing.
- **Django REST Framework (DRF)** – Adds REST API functionality to Django.  
- **Django REST Framework SimpleJWT** – Provides secure JWT-based authentication.  
- **MySQL + mysqlclient** – Relational database and Python connector.  
- **django-cors-headers** – Enables CORS for frontend-backend communication.  
- **python-dotenv** – Environment variables.

## 🚀 Backend Setup (Django + MySQL)
---

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
   # Edit .env with SECRET_KEY and database settings
   ```
   
   Generate a new secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   # Paste the output into .env as SECRET_KEY=your-generated-key
   ```

5. **Create the MySQL Database**
   ```sql
   CREATE DATABASE restaurant_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Application**
   ```bash
   python manage.py runserver
   ```
The API will be available at:
👉 http://127.0.0.1:8000/