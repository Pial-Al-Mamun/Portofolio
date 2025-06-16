from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext

from ..config import Config

from typing import Any

load_dotenv()


class SecurityService:
    """
    Consolidated security operations including:
    - JWT token creation/verification
    - Password hashing/verification
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, user_id: str) -> str:
        return jwt.encode(
            {"sub": user_id}, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
        )
        
    def verify_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
