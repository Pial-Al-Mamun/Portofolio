from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class RegisteringUser(BaseModel):
    username: str
    email: EmailStr
    password: str

