from fastapi import status
from fastapi import HTTPException

from enum import StrEnum


class ErrorMessage(StrEnum):
    USER_ALREADY_EXISTS = "User already exists"
    USER_NOT_FOUND = "User not found"
    PASSWORD_INCORRECT = "Password is incorrect"


error_http_status_map = {
    ErrorMessage.USER_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
    ErrorMessage.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorMessage.PASSWORD_INCORRECT: status.HTTP_401_UNAUTHORIZED,
}


def raise_http_error(message: ErrorMessage):
    try:
        status_code = error_http_status_map[message]
    except KeyError:
        raise RuntimeError(f"Missing HTTP status mapping for: {message}")
    
    raise HTTPException(
        status_code=status_code,
        detail=message,
    )

