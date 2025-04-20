from db.database import SessionLocal
from user.domain.repository.user_repository import UserRepository
from user.domain.user import User as UserVO
from user.infra.db_models.user import User


class UserRepositoryImpl(UserRepository):
    def save(self, user: UserVO):
        """
        도메인 User에서 ORM User로 변환
        """
        new_user = User(
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

        with SessionLocal() as db:
            try:
                db.add(new_user)
                db.commit()
            finally:
                db.close()

        return new_user

    def find_by_email(self, email) -> User:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
        return user
