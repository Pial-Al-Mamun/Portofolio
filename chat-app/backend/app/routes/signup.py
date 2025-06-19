from ..schemas.auth.request import RegisteringUser
from ..DI.dependencies import AuthServiceSession
from ..exceptions.exception import ErrorMessage


from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status


router = APIRouter()


@router.post("/signup")
async def signup(user: RegisteringUser, auth_service: AuthServiceSession):
    result = await auth_service.signup_user(user)

    if isinstance(result, ErrorMessage):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result.value)

    return status.HTTP_201_CREATED
