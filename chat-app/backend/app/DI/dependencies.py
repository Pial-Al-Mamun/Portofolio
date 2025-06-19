from app.services.auth_service import AuthService

from typing import Annotated
from fastapi import Depends




def get_auth_service() -> AuthService:
    return AuthService()


AuthServiceSession = Annotated[AuthService, Depends(get_auth_service)]

