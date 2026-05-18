# Ecommerce API

Simple MVP ecommerce backend API built with FastAPI, SQLAlchemy ORM, and PostgreSQL.

## Features
- Login 
- JWT Authentication (Access token and Refresh token)
- Users creation
- Product Management
- Shopping cart
- Order Creation
- Minimal payments integration with PayPal Sandbox (Creation and Capture)
- REST API

## Tech Stack
- FastAPI / Python
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentitacion
- Pydantic

## Project Structure
app/
├── core/
├── db/
├── dependencies/
├── models/
├── repositories/
├── schemas/
└── services/

## Instalation
Clone the repository

git clone <https://github.com/isaiMiranda1998/LizBuy.git>

Install the dependencies using the next PIP package manager command <pip install -r requirements.txt>

## Enviroment Variables

Create a '.env' file:

JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=
JWT_REFRESH_TOKEN_EXPIRE_DAYS=
DATABASE_URL=
PAYPAL_API_KEY=
PAYPAL_SECRET_KEY=

## Run the Project

Use uvicorn to run the project locally with the command <python -m uvicorn app.main:app --reload>

## API Endpoints

### Auth

POST /auth/register
POST /auth/login
POST /auth/register

### Users
PATCH /users
PUT /users
DELETE /users

### Products

GET /products
GET /products/{product_id}
POST /products
PUT /products/{product_id}
DELETE /products/{product_id}

### Carts

GET /carts
DELETE /carts
POST /carts/items
POST /carts/items/{cart_item_id}

### Orders

GET /orders/{order_id}
POST /orders/checkout

### Payments

POST /payments/paypal/checkout/{order_id}
POST /payments/paypal/capture/{paypal_order_id}

## Authentication

Protected routes require JWT token:
Authorization: Bearer <token>

## Future Improvements

- Deployment with Docker
- Rate limiting
- Logging
- Caching with Redis
- Implementation of automated tests with GitHub Actions