from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.product import Product
from decimal import Decimal
import uuid
from typing import Any

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_products(self):
        return self.db.execute(select(Product)).scalars().all()
    
    def get_product_by_id(self, product_id: uuid.UUID):
        return self.db.get(Product, product_id)
    
    def create_product(self, product: Product): 
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product
    
    def update_product(self, product: Product, *, name: str, price: Decimal, stock: int, description: str, active: bool):
        product.name = name
        product.price = price
        product.stock = stock
        product.description = description
        product.active = active

        self.db.commit()
        self.db.refresh(product)

        return product
    
    def partial_update_product(self, product: Product, **kwargs: Any):
        for attribute, value in kwargs.items():
            setattr(product, attribute, value)

        self.db.commit()
        self.db.refresh(product)

        return product
    
    def delete_product(self, product: Product):
        self.db.delete(product)
        self.db.commit()