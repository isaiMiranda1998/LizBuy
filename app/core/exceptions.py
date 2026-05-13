#Product Exceptions
class ProductNotFoundError(Exception):
    pass

#Auth Exceptions
class InvalidCredentials(Exception):
    pass

class InvalidToken(Exception): 
    pass

#User Exceptions
class EmailExists(Exception):
    pass

class UsernameExists(Exception):
    pass

class UserNotFoundError(Exception):
    pass

#Cart Exceptions
class CartNotFoundError(Exception):
    pass

class InvalidProductQuantity(Exception):
    pass

class CartItemNotFoundError(CartNotFoundError):
    pass

#Order Exceptions
class InvalidCurrency(Exception):
    pass

class InvalidOrderStatus(Exception):
    pass

class OrderNotFoundError(Exception): 
    pass

#Paypal Exceptions
class PayPalException(Exception):
    pass

class PayPalNotFoundOrder(PayPalException):
    pass