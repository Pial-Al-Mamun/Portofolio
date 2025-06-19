from fastapi import status


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
