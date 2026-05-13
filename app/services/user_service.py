from app.repositories.user_repository import UserRepository
from app.repositories.cart_repository import CartRepository
from app.schemas.user import UserRead, UserResponse, UserPartialUpdate
from app.core.exceptions import EmailExists, UsernameExists, UserNotFoundError
from app.models.cart import Cart
from app.models.user import User
from app.core.security import hash_password
from .helpers import parse_id

class UserService:
    def __init__(self, user_repo: UserRepository, cart_repo: CartRepository):
        self.user_repo = user_repo
        self.cart_repo = cart_repo

    def get_user(self, user_id: str):
        return UserResponse.model_validate(self._get_user_by_id(user_id))

    def create_user(self, user_data: UserRead):
        if self.user_repo.get_user_by_username(user_data.username):
            raise EmailExists(f"The username {user_data.username} already exists")
        
        if self.user_repo.get_user_by_email(user_data.email):
            raise UsernameExists(f"There's already another user with the email {user_data.email}")
        
        user_model = User(
            username = user_data.username,
            email = user_data.email,
            name = user_data.name,
            password = hash_password(user_data.password)
        )

        user_response_model = self.user_repo.create(user_model)

        cart_model = Cart(
            user_id = user_response_model.id
        )

        self.cart_repo.create_cart(cart_model)

        return UserResponse.model_validate(user_response_model)
    
    def partial_update_user(self, user_id: str, user_update: UserPartialUpdate):
        user = self._get_user_by_id(user_id)

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        return UserResponse.model_validate(self.user_repo.partial_update_user(user, **update_data))
    
    def update_user(self, user_id: str, user_update: UserRead):
        user = self._get_user_by_id(user_id)
        
        response_model = self.user_repo.update_user(user, user_update.username, user_update.email, user_update.name, hash_password(user_update.password))

        return UserResponse.model_validate(response_model)
    
    def delete_user(self, user_id: str):
        user = self._get_user_by_id(user_id)
        self.user_repo.delete_user(user)

    def _get_user_by_id(self, user_id: str):
        user = self.user_repo.get_user_by_id(parse_id(user_id))

        if not user:
            raise UserNotFoundError(f"The username with ID {user_id} doesn't exist")
        
        return user

