from dependency_injector import containers, providers

from auth.application.auth_service import AuthService
from auth.application.auth_token_service import AuthTokenService
from auth.application.jwt_token_provider import JwtTokenProvider
from auth.infra.repository.redis_refresh_token_repository import (
    RedisRefreshTokenRepository,
)
from book.application.book_service import BookService
from book.infra.repository.mysql_book_repository import MysqlBookRepository
from user.application.user_service import UserService
from user.application.user_validator import UserValidator
from user.infra.repository.user_repository_impl import UserRepositoryImpl


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user", "auth", "book"],
    )

    user_repository = providers.Factory(UserRepositoryImpl)

    user_validator = providers.Factory(UserValidator)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        user_validator=user_validator,
    )

    refresh_token_repository = providers.Factory(RedisRefreshTokenRepository)
    jwt_token_provider = providers.Factory(
        JwtTokenProvider, refresh_token_repository=refresh_token_repository
    )
    auth_token_service = providers.Factory(
        AuthTokenService,
        jwt_token_provider=jwt_token_provider,
    )
    auth_service = providers.Factory(
        AuthService, user_service=user_service, auth_token_service=auth_token_service
    )

    book_repository = providers.Factory(MysqlBookRepository)
    book_service = providers.Factory(BookService, book_repository=book_repository)
