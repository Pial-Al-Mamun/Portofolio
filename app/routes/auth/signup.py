from ...entities.tables import User
from ...database.core import SessionLocal

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

router = APIRouter()


class RegisteringUser(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/register")
async def register(user: RegisteringUser):
    with SessionLocal() as session:

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            username=user.username, email=user.email, password=hashed_password
        )
        
        session.add(new_user)
        session.commit()