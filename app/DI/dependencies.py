from app.services.auth_service import AuthService
from app.services.token_service import SecurityService


def get_token_service() -> SecurityService:
    return SecurityService()


def get_auth_service() -> AuthService:
    return AuthService()