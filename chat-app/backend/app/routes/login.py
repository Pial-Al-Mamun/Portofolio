from app.schemas.auth.request import LoginUser
from app.DI.dependencies import AuthServiceSession
from app.exceptions.exception import ErrorMessage, error_http_status_map

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from typing import Any

router = APIRouter()


@router.post("/login")
async def login(
    user: LoginUser,
    auth_service: AuthServiceSession,
    response: Response,
) -> Any:
    result = await auth_service.login_user(user)

    if isinstance(result, ErrorMessage):
        raise HTTPException(
            status_code=error_http_status_map.get(result, status.HTTP_400_BAD_REQUEST),
            detail=result.value,
        )


    return {"access_token": result, "token_type": "bearer"}
