from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.auth import RefreshToken
import uuid

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_refresh_token_by_id(self, token_id: uuid.UUID):
        stmt = select(RefreshToken).where(RefreshToken.token_id == token_id).options(selectinload(RefreshToken.user))
        return self.db.execute(stmt).scalar()
    
    def save_refresh_token(self, refresh_token: RefreshToken):
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def revoke(self, token_id: uuid.UUID):
        token = self.get_refresh_token_by_id(token_id)

        if token is None:
            raise ValueError("Token not found")
        
        token.revoked = True
        self.db.commit()

    
