from fastapi import HTTPException, status
from dependency_injector.wiring import inject
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from auth.domain.repository.refresh_token_repository import RefreshTokenRepository
from auth.domain.role import Role

from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))


class JwtTokenProvider:
    @inject
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    def create_token(
        self, payload: dict, role: Role, expires_delta: timedelta, secret_key: str
    ) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        payload.update({"role": role, "exp": expire})
        return jwt.encode(payload, secret_key, algorithm=ALGORITHM)

    def create_access_token(self, user_id: str) -> str:
        payload = {"id": user_id}
        return self.create_token(
            payload,
            Role.USER,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            ACCESS_SECRET_KEY,
        )

    async def create_refresh_token(self, user_id: str) -> str:
        payload = {"id": user_id}

        refresh_token = self.create_token(
            payload,
            Role.USER,
            timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
            REFRESH_SECRET_KEY,
        )

        await self.refresh_token_repository.save(
            user_id, refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )

        return refresh_token

    def decode_token(self, token: str, secret_key: str) -> dict:
        try:
            return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="올바르지 않은 토큰입니다.",
            )

    def get_user_from_access_token(self, token: str) -> dict:
        return self.decode_token(token, ACCESS_SECRET_KEY)

    def get_user_from_refresh_token(self, token: str) -> dict:
        return self.decode_token(token, REFRESH_SECRET_KEY)

    async def validate_refresh_token(self, token: str) -> bool:
        payload = self.decode_token(token, REFRESH_SECRET_KEY)
        user_id = payload.get("id")

        if not await self.refresh_token_repository.exists_by_user_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token을 찾을 수 없습니다.",
            )
        return True
