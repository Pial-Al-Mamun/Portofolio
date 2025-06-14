from app.services.auth_service import AuthService
from app.services.token_service import TokenService


def get_token_service() -> TokenService:
    return TokenService()


def get_auth_service() -> TokenService:
    return AuthService()