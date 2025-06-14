from dotenv import load_dotenv
import jwt
import os


load_dotenv()


class TokenService:
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    def __init__(self):
        self.secret = TokenService.SECRET_KEY
        self.algorithm = TokenService.ALGORITHM

    def create(self, user_id: str) -> str:
        return jwt.encode(user_id, self.secret, self.algorithm)

    def verify(self, token: str) -> dict:
        return jwt.decode(token, self.secret, [self.algorithm])
