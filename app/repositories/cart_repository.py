from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.cart import Cart, CartItem
from datetime import datetime
import uuid

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_user_id(self, user_id: uuid.UUID): 
        stmt = select(Cart).where(Cart.user_id == user_id).options(
            selectinload(Cart.cart_items),
            selectinload(Cart.user)
        )
        return self.db.execute(stmt).scalar()
    
    def get_cart_by_id(self, cart_id: uuid.UUID):
        stmt = select(Cart).where(Cart.id == cart_id).options(
            selectinload(Cart.cart_items),
            selectinload(Cart.user)
        )
        return self.db.execute(stmt).scalar()

    def create_cart(self, cart: Cart):
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)

        return cart
    
    def update_cart(self, cart: Cart, updated_at: datetime):
        cart.updated_at = updated_at

        self.db.commit()
        self.db.refresh(cart)

        return cart
    
    def empty_cart(self, cart: Cart):
        cart_items = cart.cart_items
        for cart_item in cart_items:
            self.db.delete(cart_item)
        
        self.db.commit()
    
    def get_cart_item_by_id(self, cart_item_id: uuid.UUID):
        stmt = select(CartItem).where(CartItem.id == cart_item_id).options(
            selectinload(CartItem.cart),
            selectinload(CartItem.product)
        )
        return self.db.execute(stmt).scalar()
    
    def create_cart_item(self, cart_item: CartItem):
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)

        return cart_item
    
    def update_cart_item(self, cart_item: CartItem, quantity: int, updated_at: datetime):
        cart_item.quantity = quantity
        cart_item.updated_at = updated_at

        self.db.commit()
        self.db.refresh(cart_item)

        return cart_item