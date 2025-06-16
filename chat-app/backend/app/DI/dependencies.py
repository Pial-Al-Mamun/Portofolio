from app.services.auth_service import AuthService
from app.services.security_service import SecurityService

from typing import Annotated
from fastapi import Depends


def get_security_service() -> SecurityService:
    return SecurityService()


def get_auth_service() -> AuthService:
    return AuthService()


AuthServiceSession = Annotated[AuthService, Depends(get_auth_service)]

