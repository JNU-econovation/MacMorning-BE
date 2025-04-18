from fastapi import status
from core.exception.custom_exception import BusinessException


class UserNotFoundException(BusinessException):
    def __init__(self):
        super().__init__(
            code="USER001",
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="해당하는 사용자가 존재하지 않습니다.",
        )


class InvalidCredentialsException(BusinessException):
    def __init__(self):
        super().__init__(
            code="USER002",
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다.",
        )


class UserAlreadyExistsException(BusinessException):
    def __init__(self):
        super().__init__(
            code="USER003",
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 이메일입니다.",
        )
