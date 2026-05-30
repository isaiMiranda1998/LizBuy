from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.dependencies.cart import get_cart_repository
from app.dependencies.product import get_product_service
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated

def get_order_repository(db: Annotated[Session, Depends(get_db)]):
    return OrderRepository(db)

def get_order_service(order_repository: Annotated[OrderRepository, Depends(get_order_repository)], cart_repository: Annotated[CartRepository, Depends(get_cart_repository)], product_service: Annotated[ProductService, Depends(get_product_service)]):
    return OrderService(order_repository, cart_repository, product_service)