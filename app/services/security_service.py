from dotenv import load_dotenv
import jwt
import os
from passlib.context import CryptContext

load_dotenv()

class SecurityService:
    """
    Consolidated security operations including:
    - JWT token creation/verification
    - Password hashing/verification
    """
    
    def __init__(self):
        # JWT Configuration
        self.jwt_secret = os.getenv("JWT_SECRET_KEY")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

    def create_access_token(self, user_id: str) -> str:
        return jwt.encode(
            {"sub": user_id},
            self.jwt_secret,
            algorithm=self.jwt_algorithm
        )

    def verify_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.jwt_secret,
            algorithms=[self.jwt_algorithm]
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)