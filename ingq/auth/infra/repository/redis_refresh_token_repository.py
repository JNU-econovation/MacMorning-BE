from auth.domain.repository.refresh_token_repository import RefreshTokenRepository
from db.redis_cache import redis_cache


class RedisRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self):
        self.prefix = "refresh:"

    async def save(self, user_id: str, token: str, expire: int):
        key = f"{self.prefix}{user_id}"
        await redis_cache.set(key, token)
        await redis_cache.expire(key, expire)

    async def get(self, user_id: str) -> str:
        key = f"{self.prefix}{user_id}"
        return await redis_cache.get(key)

    async def delete(self, user_id: str):
        key = f"{self.prefix}{user_id}"
        await redis_cache.delete(key)

    async def exists_by_user_id(self, user_id: str) -> bool:
        key = f"{self.prefix}{user_id}"
        return await redis_cache.exists(key)
