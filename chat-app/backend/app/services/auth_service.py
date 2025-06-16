from ..schemas.auth.request import LoginUser, RegisteringUser
from .security_service import SecurityService
from ..entities.tables import User
from ..database.core import get_async_db
from ..DI.dependencies import get_security_service
from ..exception import ErrorMessage

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Optional


class AuthService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_async_db),
        security_service: SecurityService = Depends(get_security_service),
    ):
        self.db = db
        self.security = security_service

    async def signup_user(self, user: RegisteringUser) -> Optional[ErrorMessage]:
        """Returns User if created, None if email exists"""

        existing_user = await self.db.execute(
            select(User).where(User.email == user.email)
        )

        if existing_user.scalar_one_or_none():
            return ErrorMessage.USER_ALREADY_EXISTS

        hashed = self.security.hash_password(user.password)

        new_user = User(
            email=user.email, username=user.username, hashed_password=hashed
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

    async def login_user(self, credentials: LoginUser) -> str | ErrorMessage:
        """Returns token if auth is valid, otherwise return an string Enum with error details"""

        result = await self.db.execute(
            select(User).where(User.email == credentials.email)
        )

        user = result.scalar_one_or_none()

        if not user:
            return ErrorMessage.USER_NOT_FOUND

        if not self.security.verify_password(
            credentials.password, user.hashed_password
        ):
            return ErrorMessage.PASSWORD_INCORRECT

        token = self.security.create_access_token(user.id)
        return token
