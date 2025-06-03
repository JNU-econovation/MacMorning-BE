from fastapi import status

from core.exception.custom_exception import BusinessException


class IllustDoesNotBelongToBookException(BusinessException):
    def __init__(self):
        super().__init__(
            code="ILLU001",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="해당 책에 속하는 이미지가 아닙니다.",
        )
