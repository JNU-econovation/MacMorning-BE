from dependency_injector.wiring import inject

from auth.application.jwt_token_provider import JwtTokenProvider
from auth.dto.schemas import AuthToken
from auth.utils.mapper import AuthMapper
from core.setting.load_env import ACCESS_TOKEN_EXPIRE_MINUTES

ACCESS_TOKEN_EXPIRE_SECONDS = ACCESS_TOKEN_EXPIRE_MINUTES * 60


class AuthTokenService:
    @inject
    def __init__(self, jwt_token_provider: JwtTokenProvider):
        self.jwt_token_provider: JwtTokenProvider = jwt_token_provider

    async def generate_auth_token(self, user_id: str) -> AuthToken:
        access_token = self.jwt_token_provider.create_access_token(user_id)
        refresh_token = await self.jwt_token_provider.create_refresh_token(user_id)
        token_expires_in = ACCESS_TOKEN_EXPIRE_SECONDS

        auth_token = AuthMapper.to_auth_token_response(
            access_token, refresh_token, token_expires_in
        )

        return auth_token
