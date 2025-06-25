from fastapi import status

from core.exception.custom_exception import BusinessException


class ChoiceException(BusinessException):
    pass


class ChoiceNotFoundException(ChoiceException):
    def __init__(self):
        super().__init__(
            code="CHOICE001",
            status_code=status.HTTP_404_NOT_FOUND,
            detail="선택지를 찾을 수 없습니다.",
        )
