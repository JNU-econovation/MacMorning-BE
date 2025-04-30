from fastapi import status

from core.exception.custom_exception import BusinessException


class StoryException(BusinessException):
    pass


class DuplicatePageNumberException(StoryException):
    def __init__(self):
        super().__init__(
            code="STORY001",
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 페이지 번호입니다.",
        )


class InvalidBookProgressException(StoryException):
    def __init__(self):
        super().__init__(
            code="STORY002",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="완성된 책에는 새로운 스토리를 추가할 수 없습니다.",
        )


class InvalidChoiceException(StoryException):
    def __init__(self):
        super().__init__(
            code="STORY003",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="일반 모드에서는 is_success가 True여야 합니다.",
        )


class InvalidUserAccessException(StoryException):
    def __init__(self):
        super().__init__(
            code="STORY004",
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 책에 대한 접근 권한이 없습니다.",
        )
