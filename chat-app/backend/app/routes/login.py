from ..schemas.auth import LoginUser
from ..DI.dependencies import AuthServiceSession
from ..exception import ErrorMessage, error_http_status_map

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

router = APIRouter()


@router.post("/login")
async def login(
    user: LoginUser,
    auth_service: AuthServiceSession,
    response: Response,
):
    result = await auth_service.login_user(user)

    if isinstance(result, ErrorMessage):
        raise HTTPException(
            status_code=error_http_status_map.get(result, status.HTTP_400_BAD_REQUEST),
            detail=result.value,
        )

    response.set_cookie("auth", result, samesite="lax")

    return {"access_token": result, "token_type": "bearer"}
