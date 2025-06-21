from .schemas import RegisteringUser, LoginUser
from .service import AuthService
from app.database.core import AsyncDBSession

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from typing import Any

auth_route = APIRouter()


@auth_route.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user: RegisteringUser,
    db: AsyncDBSession,
) -> Any:
    service = AuthService(db)
    await service.signup_user(user)
    return JSONResponse(
        content={"message": "User created"}, status_code=status.HTTP_201_CREATED
    )


@auth_route.post("/login")
async def login(
    user: LoginUser,
    db: AsyncDBSession,
    response: Response,
) -> Any:
    service = AuthService(db)

    result = await service.login_user(user)

    print(result)

    return {"access_token": "dummy_token", "token_type": "bearer"}


@auth_route.post("/refresh")
def refresh_token():
    pass
