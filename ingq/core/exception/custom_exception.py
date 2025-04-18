from starlette.exceptions import HTTPException as StarletteHTTPException


class BusinessException(StarletteHTTPException):
    def __init__(self, status_code: int, code: str, detail: str):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)
