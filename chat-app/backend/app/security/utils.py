import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

import jwt
from passlib.context import CryptContext

from ..config import env

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


# Token expiry durations
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7  # 7 days


def create_jwt_token(user_id: int, expiry_seconds: int, refresh: bool = False) -> str:
    payload: dict[str, Any] = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload=payload, key=env.JWT_SECRET_KEY, algorithm=env.JWT_ALGORITHM
    )


def create_access_token(user_id: int) -> str:
    return create_jwt_token(user_id, ACCESS_TOKEN_EXPIRE_SECONDS, refresh=False)


def create_refresh_token(user_id: int) -> str:
    return create_jwt_token(user_id, REFRESH_TOKEN_EXPIRE_SECONDS, refresh=True)


def decode_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(token, key=env.JWT_SECRET_KEY, algorithms=[env.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        logging.warning("Token expired")
    except jwt.InvalidTokenError:
        logging.warning("Invalid token")
    except Exception as e:
        logging.exception(e)

    return None
