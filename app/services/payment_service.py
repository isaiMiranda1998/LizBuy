from app.repositories.payment_repository import PaymentRepository
from app.services.order_service import OrderService
from app.core.exceptions import PayPalException, PayPalNotFoundOrder
from app.core.config import paypal_settings
from app.schemas.payment import PayPalCheckoutResponse
from app.schemas.order import OrderResponse
from app.schemas.payment import PaymentResponse
from app.models.payment import Payment, Providers, PaymentStatus
from .helpers import generate_uuid4
import httpx
from typing import Any, cast
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, order_service: OrderService):
        self.order_service = order_service
        self.payment_repo = payment_repo

    def create_paypal_order(self, order_id: str):
        order = self.order_service.get_order(order_id)

        params: dict[str, Any] = {
            "headers": {
                "Authorization": f"Bearer {self._get_paypal_access_token()}",
                "PayPal-Request-Id": f"{generate_uuid4()}"
            },
            "json": {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": f"{order.total_amount}"
                        }
                    } 
                ]
            }
        }

        response = self._fetch("https://api-m.sandbox.paypal.com/v2/checkout/orders", "post", **params)
        self._create_payment_order(order, Providers.PAYPAL, response.json()["id"])
        
        return PayPalCheckoutResponse(
            payment_id = response.json()["id"],
            approval_url = self._get_approve_link(cast(list[dict[str, str]], response.json()["links"]))
        )

    def capture_paypal_order(self, paypal_order_id: str):
        paypal_order = self.payment_repo.get_payment_by_provider_payment_id(paypal_order_id)

        if not paypal_order:
            raise PayPalNotFoundOrder(f"Paypal order with ID {paypal_order_id} doesn't exist")

        headers: dict[str, Any] = {
            "Authorization": f"Bearer {self._get_paypal_access_token()}",
            "PayPal-Request-Id": f"{generate_uuid4()}"
        }

        json = {}

        self._fetch(f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order.provider_payment_id}/capture", "post", headers=headers, json=json)
        self.order_service.confirm_paid_order(str(paypal_order.order_id))
        
        return PaymentResponse.model_validate(
            self.payment_repo.partial_update_payment(
                paypal_order, 
                status = PaymentStatus.PAID, 
                paid_at = datetime.now(timezone.utc)
            )
        )

    def _create_payment_order(self, order: OrderResponse, provider: Providers, provider_payment_id: str):
        payment_model = Payment(
            id = generate_uuid4(),
            order_id = order.id,
            provider = provider,
            provider_payment_id = provider_payment_id,
            status = PaymentStatus.PENDING,
            amount = order.total_amount,
            currency = order.currency
        )

        self.payment_repo.create_payment_order(payment_model)
            
    def _get_paypal_access_token(self):
        root = Path(__file__).parent / "paypal_access_token.txt"
        root.touch()
        
        with open(root, mode="r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
                expiration_date = datetime.fromisoformat(data["expires_in"])

                if datetime.now(timezone.utc) >= expiration_date:
                    file.seek(0)
                    file.truncate()
                    data = self._paypal_authentication()
                    json.dump(data, file, ensure_ascii=False, indent=4)

            except json.JSONDecodeError:
                data = self._paypal_authentication()
                json.dump(data, file, ensure_ascii=False, indent=4)

        return data["access_token"]

    def _paypal_authentication(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "auth": (paypal_settings.api_key, paypal_settings.secret_key),
            "data": {"grant_type": "client_credentials"}
        }

        response = self._fetch("https://api-m.sandbox.paypal.com/v1/oauth2/token", "post", **params)
        expiration_date = datetime.now(timezone.utc) + timedelta(seconds=response.json()["expires_in"])

        return {
            "access_token": response.json()["access_token"], 
            "expires_in": expiration_date.isoformat()
        }

    def _fetch(self, url: str, method: str, **kwargs: Any):
        try:
            client = httpx.Client(base_url=url)
            response = client.request(method, "", **kwargs)
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as ex:
            raise PayPalException(f"Paypal returned an HTTP error {str(ex)}: {ex.response.status_code}") 
        except httpx.TimeoutException as ex:
            raise PayPalException("The request to PayPal timeout")
        except httpx.ConnectError as ex:
            raise PayPalException("Unable to establish a connection with Paypal")
        except httpx.RequestError as ex:
            raise PayPalException(f"An unexpected error ocurred while sending the request to PayPal: {str(ex)}")
        
    def _get_approve_link(self, order_links: list[dict[str, str]]):
        link = ""
        for value in order_links:
            if value["rel"] == "approve":
                link = value["href"] 
                break

        return link

