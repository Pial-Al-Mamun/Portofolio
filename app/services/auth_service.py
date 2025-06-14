from ..schemas.auth.request import LoginUser, RegisteringUser
from .security_service import SecurityService
from ..entities.tables import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Tuple


class AuthService:
    def __init__(self, db: AsyncSession, security_service: SecurityService):
        self.db = db
        self.security = security_service

    async def signup_user(self, user: RegisteringUser) -> Optional[User]:
        """Returns User if created, None if email exists"""
        
        existing_user = await self.db.execute(
            select(User).where(User.email == user.email)
        )
        
        if existing_user.scalar_one_or_none():
            return None

        hashed = self.security.hash_password(user.password)
        
        new_user = User(
            email=user.email, username=user.username, hashed_password=hashed
        )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        
        return new_user

    async def login_user(self, credentials: LoginUser) -> Optional[Tuple[User, str]]:
        """Returns (User, token) if valid, None otherwise"""
        
        result = await self.db.execute(
            select(User).where(User.email == credentials.email)
        )
        
        user = result.scalar_one_or_none()

        if not user or not self.security.verify_password(
            credentials.password, user.hashed_password
        ):
            return None

        token = self.security.create_access_token(user.id)
        return user, token
