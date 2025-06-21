from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException
from fastapi import status

from app.exception import InvalidToken
from app.exception import AccessTokenRequired
from app.exception import RefreshTokenRequired
from .utils import decode_token

from typing import Optional
from typing import Any


class TokenBearer(HTTPBearer, ABC):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)

        if creds is None:
            return

        token = creds.credentials

        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not self.verify_token_data(token_data):
            raise InvalidToken()

    @abstractmethod
    def verify_token_data(self, token_data: dict[str, Any]):
        pass


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()
