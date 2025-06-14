from typing import Annotated, AsyncGenerator
from fastapi import Depends

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)

from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# change url to make async request with sqlalchemy
DATABASE_URL = (
    os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://", 1)
    if os.getenv("DATABASE_URL")
    else None
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


AsyncDBSession = Annotated[AsyncSession, Depends(get_async_db)]
