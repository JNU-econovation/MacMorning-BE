from ulid import ULID
from datetime import datetime
from user.domain.user import User as UserVO
from user.domain.repository.user_repository import UserRepository
from user.application.user_validator import UserValidator
from user.utils.crypto import Crypto

from user.dto.schemas import SignUpRequest
from user.domain.provider import Provider

from user.utils.mapper import UserMapper

from utils.logging import logging

from dependency_injector.wiring import inject

from fastapi import HTTPException, status


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
        self.logging = logging.getLogger()

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="해당하는 사용자가 없습니다.",
            )

        return UserMapper.to_domain_user(user)

    def find_user_by_email_and_password(self, email: str, password: str) -> UserVO:
        user = self.user_repository.find_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 일치하지 않습니다.",
            )

        try:
            self.crypto.verify(password, user.password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 일치하지 않습니다.",
            )

        return UserMapper.to_domain_user(user)
