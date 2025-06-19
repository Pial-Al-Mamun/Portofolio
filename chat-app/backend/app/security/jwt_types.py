from typing import TypedDict
from datetime import datetime


class JWTPayload(TypedDict):
    user_id: int
    exp: datetime
    jti: str
    refresh: bool


class RefreshTokenPayload(TypedDict):
    user_id: int
    exp: int  # Expiration timestamp (Unix time)
    jti: str  # JWT ID for refresh token identification
