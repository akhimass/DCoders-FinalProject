# 🥪 Restaurant Order Management API

A full-featured FastAPI backend for managing a sandwich restaurant, built for Software Engineering course final project. This system handles menu items, customers, ingredients, reviews, orders, inventory, and promotional codes.

---

## 🚀 Features

### ✅ Customer Experience
- Place orders **without an account**
- Apply **promotional codes** at checkout
- Track order status via **tracking number**
- Select **order type**: takeout or delivery
- Search menu by keyword or **dietary tag** (e.g., vegetarian)
- Submit **ratings and reviews** for items

### ✅ Restaurant Staff Tools
- Full **CRUD support** for:
  - Menu Items
  - Customers
  - Ingredients
  - Reviews
  - Orders
- Real-time **ingredient depletion check**
- Revenue tracking by **date range**
- Identify **popular/unpopular dishes** via reviews
- Manage **promotional codes** with expiration logic
- View **filtered order lists**

---

## 🧪 Tech Stack

- **FastAPI** (backend framework)
- **SQLAlchemy** (ORM for MySQL)
- **Pydantic** (data validation)
- **MySQL** (database)
- **Pytest** (unit testing)

🔍 API Endpoints

Swagger UI available at: http://127.0.0.1:8000/docs

🧾 Customers
	•	GET /customers/
	•	PUT /customers/{id}

🍔 Menu Items
	•	POST /menu-items/
	•	GET /menu-items/
	•	PUT /menu-items/{id}
	•	DELETE /menu-items/{id}
	•	GET /menu-items/search?query=vegetarian

🧂 Ingredients
	•	POST /ingredients/
	•	PUT /ingredients/{id}

📦 Orders
	•	POST /orders/ → (ingredient depletion + promo code logic applied)
	•	GET /orders/ → (filter by date)
	•	GET /orders/revenue?start=YYYY-MM-DD&end=YYYY-MM-DD
	•	GET /orders/{id}

🧾 Reviews
	•	POST /reviews/
	•	DELETE /reviews/{id}

🎟 Promo Codes
	•	POST /promo-codes/
	•	GET /promo-codes/
	•	Auto-check for expiration_date on usage

👥 Contributors
	•	Akhi Chappidi
 	•	Dave Nallipogu
	•	Tyler Weber
 	•	Tithi Thakkar
