# pyright: reportUnusedFunction=false

from typing import Any, Callable, Awaitable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging


class ChatAppExceptions(Exception):
    """Base class for all application-specific exceptions."""
    pass


class ResourceNotFound(ChatAppExceptions):
    """Requested resource was not found."""
    pass


class ConflictError(ChatAppExceptions):
    """Conflict error, e.g., resource already exists."""
    pass


class UnauthorizedError(ChatAppExceptions):
    """Unauthorized access error."""
    pass


class InvalidToken(ChatAppExceptions):
    """User has provided an invalid or expired token"""
    pass


class RevokedToken(ChatAppExceptions):
    """User has provided a token that has been revoked"""
    pass


class AccessTokenRequired(ChatAppExceptions):
    """User has provided a refresh token when an access token is needed"""
    pass


class RefreshTokenRequired(ChatAppExceptions):
    """User has provided an access token when a refresh token is needed"""
    pass


class UserAlreadyExists(ConflictError):
    """User already exists."""
    pass


class UserNotFound(ResourceNotFound):
    """User not found."""
    pass


class PasswordIncorrect(UnauthorizedError):
    """Incorrect password."""
    pass


def create_exception_handler(
    status_code: int, initial_detail: dict[str, Any]
) -> Callable[[Request, Exception], Awaitable[JSONResponse]]:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_app_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(
        ResourceNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Resource not found",
                "error_code": "resource_not_found",
            },
        ),
    )
    app.add_exception_handler(
        ConflictError,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "Conflict occurred",
                "error_code": "conflict_error",
            },
        ),
    )
    app.add_exception_handler(
        UnauthorizedError,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Unauthorized", "error_code": "unauthorized"},
        ),
    )

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User already exists",
                "error_code": "USER_ALREADY_EXISTS",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "USER_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        PasswordIncorrect,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Password is incorrect",
                "error_code": "PASSWORD_INCORRECT",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            content={"message": "Internal server error", "error_code": "server_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request: Request, exc: Exception):
        logging.error(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
