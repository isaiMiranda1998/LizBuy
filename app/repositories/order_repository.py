from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.order import Order, OrderItem
import uuid
from typing import Any

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order_by_id(self, order_id: uuid.UUID):
        stmt = select(Order).where(Order.id == order_id).options(
            selectinload(Order.order_items), 
            selectinload(Order.user)
        )
        return self.db.execute(stmt).scalar()
    
    def create_order(self, order: Order, order_items: list[OrderItem]):
        self.db.add(order)

        for order_item in order_items:
            self.db.add(order_item)

        self.db.commit()
        self.db.refresh(order)

        return order
    
    def partial_update_order(self, order: Order, **kwargs: Any):
        for attribute, value in kwargs.items():
            setattr(order, attribute, value)

        self.db.commit()
        self.db.refresh(order)

        return order
