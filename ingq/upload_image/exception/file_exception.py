from fastapi import status

from core.exception.custom_exception import BusinessException


class FileException(BusinessException):
    pass


class InvalidExtTypeException(FileException):
    def __init__(self):
        super().__init__(
            code="FILE001",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 파일 확장자 입니다.(png, jpg, jpeg, gif, webp) 중 하나를 사용해주세요.",
        )


class InvalidFilenameLengthException(FileException):
    def __init__(self):
        super().__init__(
            code="FILE002",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="파일 이름은 50자 이하로 입력해주세요.",
        )


class InvalidFilenameCharacterException(FileException):
    def __init__(self):
        super().__init__(
            code="FILE003",
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="파일 이름은 영문자, 숫자, 특수문자(_ . -)만 사용할 수 있습니다.",
        )
