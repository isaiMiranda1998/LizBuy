from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.user import User
import uuid

class UserRepository: 
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, user_name: str):
        stmt = select(User).where(User.username == user_name).options(
            selectinload(User.refresh_tokens),
            selectinload(User.cart), 
            selectinload(User.orders)
        )
        return self.db.execute(stmt).scalar()
    
    def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email).options(
            selectinload(User.refresh_tokens),
            selectinload(User.cart),
            selectinload(User.orders)
        )
        return self.db.execute(stmt).scalar()
    
    def get_user_by_id(self, user_id: uuid.UUID):
        stmt = select(User).where(User.id == user_id).options(
            selectinload(User.refresh_tokens),
            selectinload(User.cart),
            selectinload(User.orders)
        )
        return self.db.execute(stmt).scalar()
    
    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def partial_update_user(self, user: User, /, **kwargs: str):
        for name_field, value in kwargs.items():
            setattr(user, name_field, value)

        self.db.commit()
        self.db.refresh(user)

        return user
    
    def update_user(self, user: User, username: str, email: str, name: str, password: str):
        user.username = username
        user.email = email
        user.name = name
        user.password = password

        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()