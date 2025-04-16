from fastapi.responses import JSONResponse
from core.response.success_response import SuccessResponse
from core.exception.error_response import ErrorResponse


class ApiResponseWrapper(JSONResponse):
    def render(self, content: any) -> bytes:
        if isinstance(content, (SuccessResponse, ErrorResponse)):
            return super().render(content.model_dump())

        wrapped = SuccessResponse(success=True, data=content, error=None)
        return super().render(wrapped.model_dump())
