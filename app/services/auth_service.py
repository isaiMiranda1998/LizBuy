from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.models.auth import RefreshToken
from app.core.security import create_access_token, verify_password, create_refresh_token, verify_token
from app.core.exceptions import InvalidCredentials, InvalidToken
import uuid
from app.repositories.auth_repository import AuthRepository 
from datetime import datetime

class AuthService:
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    def login_user(self, data: LoginRequest):
        user = self.user_repo.get_user_by_username(data.username)

        if not user or not verify_password(data.password, user.password):
            raise InvalidCredentials("Invalid credentials")
        
        for token in user.refresh_tokens:
            if not token.revoked:
                self.auth_repo.revoke(token.token_id)
        
        return self._get_pair_tokens(user.id)
    
    def refresh_access_token(self, refresh_token: str):
        payload = verify_token(refresh_token)
        token_id = payload.get("jti")

        if not token_id:
            raise InvalidToken(f"Invalid token structure")
        
        token_id = uuid.UUID(token_id)
        stored_token = self.auth_repo.get_refresh_token_by_id(token_id)
        
        if not stored_token or stored_token.revoked:
            raise InvalidToken("Refresh token is not valid or has been revoked")
        
        self.auth_repo.revoke(token_id)

        return self._get_pair_tokens(stored_token.user_id)
    
    def _get_pair_tokens(self, user_id: uuid.UUID):
        access_token, refresh_token, token_id, expires_at = self._generate_tokens(user_id)

        self._save_refresh_token(token_id, user_id, expires_at)

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    def _generate_tokens(self, user_id: uuid.UUID):
        token_id = uuid.uuid4()

        access_token = create_access_token({"sub": str(user_id)})
        refresh_token, expires_at = create_refresh_token({
            "sub": str(user_id),
            "jti": str(token_id)
        })

        return access_token, refresh_token, token_id, expires_at

    def _save_refresh_token(self,  token_id: uuid.UUID, user_id: uuid.UUID, expires_at: datetime):
        refresh_token = RefreshToken(
            token_id = token_id,
            user_id = user_id,
            expires_at = expires_at,
            revoked = False
        )

        self.auth_repo.save_refresh_token(refresh_token)
    
    
