from user.domain.user import User
from user.exception.user_exceptions import UserAlreadyExistsException


class UserValidator:
    def is_user_exist(self, user: User) -> None:
        if user:
            raise UserAlreadyExistsException()
