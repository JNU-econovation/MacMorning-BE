from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from user.domain.user import User


class UserValidator:
    def is_user_exist(self, user: User) -> None:
        try:
            if user:
                raise HTTPException(
                    status_code=422, detail="이미 존재하는 이메일입니다."
                )
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"데이터베이스에서 오류가 발생했습니다.: error{e}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"알 수 없는 오류가 발생했습니다.: error{e}"
            )
