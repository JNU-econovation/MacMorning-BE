from fastapi import status

from core.exception.custom_exception import BusinessException


class BookmarkNotAllowedForInProgressBookException(BusinessException):
    def __init__(self):
        super().__init__(
            code="MARK001",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="진행중인 이야기는 북마크 기능을 쓸 수 없습니다.",
        )
