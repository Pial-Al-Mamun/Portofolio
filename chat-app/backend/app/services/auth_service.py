from ..schemas.auth.request import LoginUser
from ..schemas.auth.request import RegisteringUser
from ..entities.tables import User
from ..exceptions.exception import ErrorMessage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import Optional


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def signup_user(self, user: RegisteringUser) -> Optional[ErrorMessage]:
        """Returns ErrorMessage if error happens else return none if task is successfull"""

        existing_user = await self.db.execute(
            select(User).where(User.email == user.email)
        )

        if existing_user.scalar_one_or_none():
            return ErrorMessage.USER_ALREADY_EXISTS

        hashed = self.pwd_context.hash(user.password)

        new_user = User(
            email=user.email, username=user.username, hashed_password=hashed
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

    async def login_user(self, credentials: LoginUser) -> User | ErrorMessage:
        """Returns the User object, otherwise return a StrEnum with error details"""

        result = await self.db.execute(
            select(User).where(User.email == credentials.email)
        )

        user = result.scalar_one_or_none()

        if not user:
            return ErrorMessage.USER_NOT_FOUND

        if not self.pwd_context.verify(credentials.password, user.password):
            return ErrorMessage.PASSWORD_INCORRECT

        return user
