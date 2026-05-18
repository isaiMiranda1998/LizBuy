from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.payment import Payment
from typing import Any

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment_order(self, payment: Payment):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment
    
    def get_payment_by_provider_payment_id(self, provider_payment_id: str):
        stmt = select(Payment).where(Payment.provider_payment_id == provider_payment_id)
        return self.db.execute(stmt).scalar()
    
    def partial_update_payment(self, payment: Payment, **kwargs: Any):
        for attribute, value in kwargs.items():
            setattr(payment, attribute, value)

        self.db.commit()
        self.db.refresh(payment)

        return payment