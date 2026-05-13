from app.dependencies.product import get_product_repository
from app.repositories.product_repository import ProductRepository
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.cart_service import CartService
from app.repositories.cart_repository import CartRepository
from app.db.session import get_db
from typing import Annotated

def get_cart_repository(db: Annotated[Session, Depends(get_db)]):
    return CartRepository(db)

def get_cart_service(cart_repository: Annotated[CartRepository, Depends(get_cart_repository)], product_repository: Annotated[ProductRepository, Depends(get_product_repository)]):
    return CartService(cart_repository, product_repository)