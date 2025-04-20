from fastapi import FastAPI, Request

from core.exception.custom_exception import BusinessException, ValueException
from core.exception.error_response import ErrorDetail, ErrorResponse
from core.response.api_response_wrapper import ApiResponseWrapper
from utils.logging import get_logger

logger = get_logger("EXC")


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


async def value_exception_handler(request: Request, exc: ValueException):
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
    logger.error(f"예상치 못한 오류가 발생했습니다. 오류: {str(exc)}")
    return ApiResponseWrapper(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="EXC000",
                status=500,
                message=f"예상치 못한 오류가 발생했습니다. 오류: {str(exc)}",
            ),
        ),
    )


def register_exception_handlers(app: FastAPI):
    app.exception_handler(BusinessException)(business_exception_handler)
    app.exception_handler(ValueException)(value_exception_handler)
    app.exception_handler(Exception)(catch_all_exception_handler)
