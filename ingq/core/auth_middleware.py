from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth.application.jwt_token_provider import JwtTokenProvider
from auth.dto.schemas import CurrentUser
from core.exception.custom_exception import BusinessException
from core.exception.error_response import ErrorResponse, ErrorDetail
from auth.exception.auth_exceptions import (
    JwtTokenValidationException,
    InvalidTokenFormatException,
)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_paths, jwt_token_provider: JwtTokenProvider):
        super().__init__(app)
        self.jwt_token_provider = jwt_token_provider
        self.exempt_paths = exempt_paths

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            request.state.current_user = None
            return await call_next(request)

        token = request.headers.get("Authorization")

        try:
            if not token:
                raise JwtTokenValidationException()

            if not token.startswith("Bearer "):
                raise InvalidTokenFormatException()

            token = token.split(" ")[1]
            payload = self.jwt_token_provider.get_user_from_access_token(token)
            user_id = payload.get("id")
            role = payload.get("role")
            request.state.current_user = CurrentUser(id=user_id, role=role)

        except BusinessException as exc:
            error_detail = ErrorDetail(
                code=exc.code,
                status=exc.status_code,
                message=exc.detail,
            )
            error_response = ErrorResponse(error=error_detail)
            return JSONResponse(
                status_code=exc.status_code,
                content=error_response.model_dump(),
            )

        return await call_next(request)
