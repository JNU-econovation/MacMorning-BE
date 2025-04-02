from dependency_injector import containers, providers
from user.infra.repository.user_repository_impl import UserRepositoryImpl
from user.application.user_service import UserService
from user.application.user_validator import UserValidator


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user"],
    )

    user_repository = providers.Factory(UserRepositoryImpl)

    user_validator = providers.Factory(UserValidator)
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        user_validator=user_validator,
    )
