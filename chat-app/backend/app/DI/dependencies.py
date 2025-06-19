from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.auth_service import AuthService
from ..database.core import get_async_db

def get_auth_service(
    db: AsyncSession = Depends(get_async_db),
) -> AuthService:
    return AuthService(db)

AuthServiceSession = Annotated[AuthService, Depends(get_auth_service)]
