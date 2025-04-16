from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    status: int
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    error: ErrorDetail


def error_detail(code: str, status: int, message: str) -> ErrorDetail:
    return ErrorDetail(code=code, status=status, message=message)
