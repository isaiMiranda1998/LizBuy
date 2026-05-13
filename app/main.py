from fastapi import FastAPI
from app.routers import auth, products, carts, users, orders, payments
from app.schemas.message import ResponseMessage
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(payments.router)

@app.get("/", response_model=ResponseMessage)
def raiz():
    return {"message": "Welcome to LizBuy"}
