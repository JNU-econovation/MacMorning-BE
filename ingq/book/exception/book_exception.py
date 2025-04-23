from fastapi import status

from core.exception.custom_exception import BusinessException, ValueException


# ValueException
class InvalidCursorException(ValueException):
    def __init__(self, detail="정렬 전략과 커서 값이 일치하지 않습니다."):
        super().__init__(
            code="VAL001", status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class UnsupportedStrategyException(ValueException):
    def __init__(self, detail="지원하지 않는 order_strategy 입니다."):
        super().__init__(
            code="VAL002", status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


# BusinessException
class BookNotFoundException(BusinessException):
    def __init__(self):
        super().__init__(
            code="BOOK001",
            status_code=status.HTTP_404_NOT_FOUND,
            detail="책을 찾을 수 없습니다.",
        )
