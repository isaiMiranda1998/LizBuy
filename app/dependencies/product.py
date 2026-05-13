
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.db.session import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

def get_product_repository(db: Annotated[Session, Depends(get_db)]):
    return ProductRepository(db)

def get_product_service(product_repository: Annotated[ProductRepository, Depends(get_product_repository)]):
    return ProductService(product_repository)