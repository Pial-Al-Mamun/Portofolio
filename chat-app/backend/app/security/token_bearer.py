from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from typing import Optional
from typing import Any



class TokenBearer(HTTPBearer, ABC):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)

        token = creds.credentials

    @abstractmethod
    def verify_token_data(self, token_data: dict[str, Any]):
        pass


