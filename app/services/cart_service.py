from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.core.exceptions import CartNotFoundError, ProductNotFoundError, InvalidProductQuantity, CartItemNotFoundError
from app.schemas.cart import CartResponse, CartItemRead, CartItemResponse, CartItemUpdate
from app.models.cart import CartItem
from datetime import datetime, timezone
from .helpers import parse_id

class CartService:
    def __init__(self, cart_repo: CartRepository, product_repo: ProductRepository):
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    def get_cart_by_user_id(self, user_id: str):
        return CartResponse.model_validate(self._get_user_cart(user_id))
    
    def create_cart_item(self, user_id: str, cart_item: CartItemRead):
        cart = self._get_user_cart(user_id)
        product = self._get_product(cart_item.product_id)
        
        if cart_item.quantity > product.stock:
            raise InvalidProductQuantity(f"There's no enough stock of the product {product.name} with ID {product.id}")

        cart_item_model = CartItem(
            cart_id = cart.id,
            product_id = product.id,
            quantity = cart_item.quantity,
            unit_price = product.price
        )

        cart_item_model_response = self.cart_repo.create_cart_item(cart_item_model)
        self.cart_repo.update_cart(cart, self._now())

        return CartItemResponse.model_validate(cart_item_model_response)
    
    def update_cart_item(self, user_id: str, cart_item_id: str, cart_item_update: CartItemUpdate):
        cart = self._get_user_cart(user_id)
        cart_item = self._get_cart_item(cart_item_id)

        if cart_item.cart_id != cart.id:
            raise CartItemNotFoundError(f"Cart item does not belong to user with ID {user_id}")
        
        product = self._get_product(str(cart_item.product_id))

        if cart_item_update.quantity > product.stock:
            raise InvalidProductQuantity(f"There's no enough stock of the product {product.name} with ID {product.id}")
        
        cart_item_response_model = self.cart_repo.update_cart_item(cart_item, quantity=cart_item_update.quantity, updated_at=self._now())
        self.cart_repo.update_cart(cart, self._now())

        return CartItemResponse.model_validate(cart_item_response_model)
    
    def empty_cart(self, user_id: str):
        cart = self._get_user_cart(user_id)
        self.cart_repo.empty_cart(cart)
        self.cart_repo.update_cart(cart, self._now())

    def _get_user_cart(self, user_id: str):
        cart = self.cart_repo.get_cart_by_user_id(parse_id(user_id))

        if not cart:
            raise CartNotFoundError(f"The user id with ID {user_id} doesn't have a cart")
        
        return cart
    
    def _get_product(self, product_id: str):
        product = self.product_repo.get_product_by_id(parse_id(product_id))

        if not product:
            raise ProductNotFoundError(f"Product with id {product_id} doesn't exist")
        
        return product
    
    def _get_cart_item(self, cart_item_id: str):
        cart_item = self.cart_repo.get_cart_item_by_id(parse_id(cart_item_id))

        if not cart_item:
            raise CartItemNotFoundError(f"The cart item with ID {cart_item_id} doesn't exists")
        
        return cart_item
    
    def _now(self):
        return datetime.now(timezone.utc)



        