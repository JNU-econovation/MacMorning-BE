from datetime import datetime

from dependency_injector.wiring import inject
from ulid import ULID

from user.application.user_validator import UserValidator
from user.domain.provider import Provider
from user.domain.repository.user_repository import UserRepository
from user.domain.user import User as UserVO
from user.dto.schemas import SignUpRequest
from user.exception.user_exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
)
from user.utils.crypto import Crypto
from user.utils.mapper import UserMapper


class UserService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        user_validator: UserValidator,
    ):
        self.user_repository: UserRepository = user_repository
        self.user_validator: UserValidator = user_validator
        self.ulid = ULID()
        self.crypto = Crypto()

    def register_user(
        self,
        user: SignUpRequest,
    ):
        # ORM User Model
        _user = self.user_repository.find_by_email(user.email)

        if _user:
            # Transform ORM User Model To Domain User Model
            _user = UserMapper.to_domain_user(_user)

            self.user_validator.is_user_exist(_user)

        now = datetime.now()

        # Domain User Model
        user: UserVO = UserVO(
            id=self.ulid.generate(),
            email=user.email,
            password=self.crypto.encrypt(user.password),
            nickname=user.nickname,
            profile_image="https://www.gravatar.com/avatar/?d=mp",  # 하드코딩
            username=user.username,
            phone_number=self.crypto.phone_encrypt(user.phone_number),
            provider=Provider.LOCAL,  # 하드코딩
            created_at=now,
            updated_at=now,
        )

        self.user_repository.save(user)

        user.phone_number = self.crypto.phone_decrypt(user.phone_number)
        new_user = UserMapper.to_signup_response(user)
        return new_user

    def find_user_by_email(self, email: str) -> UserVO:
        user = self.user_repository.find_by_email(email)

        if user is None:
            raise UserNotFoundException()

        return UserMapper.to_domain_user(user)

    def find_user_by_email_and_password(self, email: str, password: str) -> UserVO:
        user = self.user_repository.find_by_email(email)

        if user is None:
            raise InvalidCredentialsException()
        try:
            self.crypto.verify(password, user.password)
        except Exception as err:
            raise InvalidCredentialsException() from err

        return UserMapper.to_domain_user(user)
