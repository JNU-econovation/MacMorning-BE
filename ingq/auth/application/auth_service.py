from auth.application.auth_token_service import AuthTokenService
from dependency_injector.wiring import inject
from auth.dto.schemas import AuthToken

from user.application.user_service import UserService


class AuthService:
    @inject
    def __init__(self, user_service: UserService, auth_token_service: AuthTokenService):
        self.user_service = user_service
        self.auth_token_service = auth_token_service

    def login(self, email: str, password: str) -> AuthToken:
        user = self.user_service.find_user_by_email_and_password(email, password)
        return self.auth_token_service.generate_auth_token(user.id)
