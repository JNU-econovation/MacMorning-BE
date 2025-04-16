from fastapi import Request, FastAPI

from core.response.api_response_wrapper import ApiResponseWrapper
from core.exception.error_response import ErrorResponse, ErrorDetail

from core.exception.custom_exception import BusinessException


async def business_exception_handler(request: Request, exc: BusinessException):
    return ApiResponseWrapper(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                status=exc.status_code,
                message=exc.detail,
            )
        ),
    )


async def catch_all_exception_handler(request: Request, exc: Exception):
    return ApiResponseWrapper(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="UNEXPECTED_EXCEPTION_0",
                status=500,
                message=f"예상치 못한 오류가 발생했습니다.\n 오류: {str(exc)}",
            ),
        ),
    )


def register_exception_handlers(app: FastAPI):
    app.exception_handler(BusinessException)(business_exception_handler)
    app.exception_handler(Exception)(catch_all_exception_handler)
