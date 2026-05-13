from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.dependencies.user import get_user_repository
from app.db.session import get_db

def get_auth_repository(db: Annotated[Session, Depends(get_db)]):
    return AuthRepository(db)

def get_auth_service(auth_repository: Annotated[AuthRepository, Depends(get_auth_repository)], user_repository: Annotated[UserRepository, Depends(get_user_repository)]):
    return AuthService(auth_repository, user_repository)