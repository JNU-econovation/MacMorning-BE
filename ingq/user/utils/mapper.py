from user.dto.schemas import SignUpResponse
from user.infra.db_models.user import User
from user.domain.user import User as UserVO


class UserMapper:
    # API 응답 값에 따라 변경
    @staticmethod
    def to_signup_response(user: User) -> SignUpResponse:
        """
        ORM User 객체를 통해 UserResponse 생성
        """

        return SignUpResponse(
            id=user.id,
            email=user.email,
            nickname=user.nickname,
            profile_image=user.profile_image,
            username=user.username,
            phone_number=user.phone_number,
            provider=user.provider,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def to_domain_user(user: User) -> UserVO:
        """
        ORM User 객체를 Domain User로 변환
        """

        return UserVO(
            id=user.id,
            email=user.email,
            password=user.password,
            nickname=user.nickname,
            profile_image=user.profile_image,
            username=user.username,
            phone_number=user.phone_number,
            provider=user.provider,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
