from .schemas import RegisteringUser, LoginUser
from app.DI.dependencies import AuthServiceSession


from fastapi import APIRouter
from fastapi import Response
from fastapi import status
from typing import Any

auth_route = APIRouter(prefix="/auth")


@auth_route.post("/signup")
async def signup(user: RegisteringUser, auth_service: AuthServiceSession):
    await auth_service.signup_user(user)

    return status.HTTP_201_CREATED


@auth_route.post("/login")
async def login(
    user: LoginUser,
    auth_service: AuthServiceSession,
    response: Response,
) -> Any:
    result = await auth_service.login_user(user)

    return {"access_token": result, "token_type": "bearer"}
