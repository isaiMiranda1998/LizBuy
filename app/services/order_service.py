from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.schemas.order import OrderResponse, OrderCreate
from .helpers import generate_uuid4, parse_id
from app.models.order import Order, OrderItem, Currencies, OrderStatus
from app.models.cart import CartItem
from app.core.exceptions import InvalidProductQuantity, InvalidCurrency, OrderNotFoundError, CartNotFoundError, InvalidOrderStatus

class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_repo: CartRepository):
        self.order_repo = order_repo
        self.cart_repo = cart_repo

    def get_order(self, order_id: str):
        return OrderResponse.model_validate(self._get_order_by_id(order_id))

    def create_order(self, user_id: str, order_data: OrderCreate):
        cart = self.cart_repo.get_cart_by_user_id(parse_id(user_id))

        if not cart:
            raise CartNotFoundError(f"The user id with ID {user_id} doesn't have a cart")

        order_currency = None if not order_data.currency else self._get_curriencies(order_data.currency)

        order_model = Order(
            id = generate_uuid4(),
            user_id = cart.user_id,
            total_amount = sum(cart_item.unit_price for cart_item in cart.cart_items),
            currency = order_currency,
            shipping_address = order_data.shipping_adress
        )

        order_item_models = [self._create_order_item(str(order_model.id), cart_item) for cart_item in cart.cart_items]
        order_model_response = self.order_repo.create_order(order_model, order_item_models)
        self.cart_repo.empty_cart(cart)

        return OrderResponse.model_validate(order_model_response)
    
    def confirm_paid_order(self, order_id: str):
        new_status = OrderStatus.PAID
        
        return OrderResponse.model_validate(
            self.order_repo.partial_update_order(
                self._get_order_by_id(order_id), 
                status=new_status
            )
        )

    def _create_order_item(self, order_id: str, cart_item: CartItem):
        product = cart_item.product

        if cart_item.quantity > product.stock:
            raise InvalidProductQuantity(f"There's no enough stock of the product {product.name} with ID {product.id}")

        order_item_model = OrderItem(
            id = generate_uuid4(),
            order_id = order_id,
            product_id = product.id,
            product_name = product.name,
            quantity = cart_item.quantity,
            unit_price = product.price,
            total_price = product.price * cart_item.quantity
        )

        return order_item_model

    def _get_order_by_id(self, order_id: str):
        order_model_response = self.order_repo.get_order_by_id(parse_id(order_id))

        if not order_model_response:
            raise OrderNotFoundError(f"Order with ID {order_id} doesn't exist")
        
        return order_model_response
    
    def _get_curriencies(self, currency: str):
        try:
            return Currencies(currency)
        except ValueError:
            raise InvalidCurrency(f"Inavalid currency {currency}")
        
    def _get_order_status(self, status: str):
        try:
            return OrderStatus(status)
        except ValueError:
            raise InvalidOrderStatus(f"Inavalid order status {status}")