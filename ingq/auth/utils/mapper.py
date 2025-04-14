from auth.dto.schemas import AuthToken


class AuthMapper:
    @staticmethod
    def to_auth_token_response(
        access_token: str, refresh_token: str, token_expires_in: int
    ) -> AuthToken:
        """
        로그인 반환 값 AuthToken 생성
        """

        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_in=token_expires_in,
        )
