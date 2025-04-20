from fastapi import status

from core.exception.custom_exception import BusinessException


class JwtTokenValidationException(BusinessException):
    def __init__(self):
        super().__init__(
            code="JWT001",
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="올바르지 않은 토큰입니다.",
        )


class RefreshTokenNotFoundException(BusinessException):
    def __init__(self):
        super().__init__(
            code="REF001",
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token을 찾을 수 없습니다.",
        )


class InvalidTokenFormatException(BusinessException):
    def __init__(self):
        super().__init__(
            code="JWT002",
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="올바르지 않은 토큰 형식입니다.",
        )
