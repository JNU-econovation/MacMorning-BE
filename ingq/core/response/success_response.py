from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

from core.exception.error_response import ErrorDetail

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[ErrorDetail]


def success_response(data: Any) -> SuccessResponse:
    return SuccessResponse(success=True, data=data, error=None)
