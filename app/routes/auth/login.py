from ...entities.tables import User
from ...database.core import SessionLocal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from sqlalchemy import select
import os
import jwt


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

router = APIRouter()


class LoginUser(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def login(user: LoginUser):
    with SessionLocal() as session:
        find_user = await select(User).where(User.email == user.email)

        is_user = await session.execute(find_user)

        if is_user is None:
            raise HTTPException()
        
        