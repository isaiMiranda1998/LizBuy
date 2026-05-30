from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.payment import PayPalCheckoutResponse, PaymentResponse
from app.dependencies.user import require_auth
from app.dependencies.payment import get_payment_service
from app.services.payment_service import PaymentService
from app.core.exceptions import PayPalException, OrderNotFoundError, PayPalNotFoundOrder
from typing import Annotated

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.post("/paypal/checkout/{order_id}", response_model=PayPalCheckoutResponse, dependencies=[Depends(require_auth)])
def create_paypal_order(order_id: str, payment_service: Annotated[PaymentService, Depends(get_payment_service)]):
    try:
        return payment_service.create_paypal_order(order_id)
    except PayPalException as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)) 
    except OrderNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    
@router.post("/paypal/capture/{paypal_order_id}", response_model=PaymentResponse, dependencies=[Depends(require_auth)]) 
def capture_paypal_order(paypal_order_id: str, payment_service: Annotated[PaymentService, Depends(get_payment_service)]):
    try:
        return payment_service.capture_paypal_order(paypal_order_id)
    except PayPalException as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)) 
    except (OrderNotFoundError, PayPalNotFoundOrder) as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))