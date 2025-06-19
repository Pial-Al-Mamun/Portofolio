import logging
import uuid
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

import jwt
from passlib.context import CryptContext

from ..config import env

from typing import Any
from typing import Optional

passwd_context = CryptContext(schemes=["bcrypt"])


ACCESS_TOKEN_EXPIRY = 60 * 60 * 24  # 1 Day
REFRESH_TOKEN_EXPIRY = 60 * 60 * 24 * 3  # 3 Day


def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_id: int, expiry: timedelta | None = None, refresh: bool = False
) -> str:
    payload: dict[str, Any] = {
        "user_id": user_id,
        "exp": datetime.now()
        + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=env.JWT_SECRET, algorithm=env.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> Optional[dict[str, Any]]:
    try:
        token_data = jwt.decode(
            jwt=token, key=env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


serializer = URLSafeTimedSerializer(secret_key=env.JWT_SECRET, salt="")


def create_url_safe_token(data: dict[str, Any]):
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)

        return token_data

    except Exception as e:
        logging.error(str(e))
