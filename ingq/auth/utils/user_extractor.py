from typing import Optional

from fastapi import Request

from auth.application.jwt_token_provider import JwtTokenProvider
from auth.dto.schemas import CurrentUser
from core.exception.custom_exception import BusinessException
from utils.logging import get_logger

logger = get_logger()


def get_optional_current_user(
    request: Request, jwt_token_provider: JwtTokenProvider
) -> Optional[CurrentUser]:
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        try:
            access_token = token.split(" ")[1]
            payload = jwt_token_provider.get_user_from_access_token(access_token)
            return CurrentUser(id=payload.get("id"), role=payload.get("role"))
        except BusinessException as exc:
            logger.info(f"BusinessException 발생: {str(exc)}")
            return None
    return None
