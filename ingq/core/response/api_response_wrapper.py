from typing import Any

from fastapi.responses import JSONResponse

from core.exception.error_response import ErrorResponse
from core.response.success_response import SuccessResponse


class ApiResponseWrapper(JSONResponse):
    def render(self, content: Any) -> bytes:
        if isinstance(content, (SuccessResponse, ErrorResponse)):
            return super().render(content.model_dump())

        wrapped = SuccessResponse(success=True, data=content, error=None)
        return super().render(wrapped.model_dump())
