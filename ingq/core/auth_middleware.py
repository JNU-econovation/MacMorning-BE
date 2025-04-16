from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from auth.application.jwt_token_provider import JwtTokenProvider
from auth.dto.schemas import CurrentUser


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_paths, jwt_token_provider: JwtTokenProvider):
        super().__init__(app)
        self.jwt_token_provider = jwt_token_provider
        self.exempt_paths = exempt_paths

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization 헤더가 없습니다.",
            )

        try:
            token = token.split(" ")[1]
            payload = self.jwt_token_provider.get_user_from_access_token(token)
            user_id = payload.get("id")
            role = payload.get("role")

            if user_id and role:
                request.state.current_user = CurrentUser(id=user_id, role=role)

            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="올바르지 않은 토큰입니다.",
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="올바르지 않은 토큰입니다.",
            )

        return await call_next(request)
