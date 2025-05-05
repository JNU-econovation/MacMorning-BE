from fastapi import status

from core.exception.custom_exception import BusinessException


class FileException(BusinessException):
    pass


class InvalidExtTypeException(FileException):
    def __init__(self):
        super().__init__(
            code="FILE001",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 파일 확장자 입니다.",
        )
