from .schemas import LoginUser, RegisteringUser
from  app.exception import UserAlreadyExists, PasswordIncorrect, UserNotFound
from app.entities.tables import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import Optional


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def signup_user(self, user: RegisteringUser) -> None:
        """Returns ErrorMessage if error happens else """

        existing_user = await self.db.execute(
            select(User).where(User.email == user.email)
        )

        if existing_user.scalar_one_or_none():
            raise UserAlreadyExists()

        hashed = self.pwd_context.hash(user.password)

        new_user = User(
            email=user.email, username=user.username, hashed_password=hashed
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

    async def login_user(self, credentials: LoginUser) -> Optional[User] :
        """Returns the User object, otherwise return a StrEnum with error details"""

        result = await self.db.execute(
            select(User).where(User.email == credentials.email)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFound()

        if not self.pwd_context.verify(credentials.password, user.password):
            raise PasswordIncorrect()

        return user
