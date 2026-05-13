from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import Annotated
from app.repositories.payment_repository import PaymentRepository
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.dependencies.order import get_order_service

def get_payment_repository(db: Annotated[Session, Depends(get_db)]): 
    return PaymentRepository(db)

def get_payment_service(payment_repository: Annotated[PaymentRepository, Depends(get_payment_repository)], order_service: Annotated[OrderService, Depends(get_order_service)]):
    return PaymentService(payment_repository, order_service)