from .schemas import RegisteringUser, LoginUser
from .service import AuthService
from .service import get_auth_service
from app.security.utils import create_access_token, create_refresh_token

from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from typing import Any

auth_route = APIRouter()


@auth_route.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user: RegisteringUser, auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    await auth_service.signup_user(user)
    return JSONResponse(
        content={"message": "User created"}, status_code=status.HTTP_201_CREATED
    )


@auth_route.post("/login")
async def login(
    user_credentials: LoginUser,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> Any:
    user = await auth_service.login_user(user_credentials)

    access_token, refresh_token = (
        create_access_token(user.id),
        create_refresh_token(user.id),
    )

    response.set_cookie(key="session_cookie", value=f"{access_token} {refresh_token}")

    return JSONResponse(
        content={"message": "Login successful"}, status_code=status.HTTP_202_ACCEPTED
    )


@auth_route.post("/refresh")
def refresh_token():
    pass
