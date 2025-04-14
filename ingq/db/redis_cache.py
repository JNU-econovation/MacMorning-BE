from typing import Optional
import redis.asyncio as redis
from redis.asyncio.client import Redis
from core.redis_config import RedisConfig


class RedisCache:
    def __init__(self):
        self.redis_cache: Optional[Redis] = redis.Redis(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            db=RedisConfig.REDIS_DATABASE,
            decode_responses=True,
        )

    # 패턴에 해당하는 모든 키 목록 조회
    async def keys(self, pattern: str):
        return await self.redis_cache.keys(pattern)

    # key-val 형태로 저장
    async def set(self, key: str, value: str):
        return await self.redis_cache.set(key, value)

    # set으로 저장된 값 조회
    async def get(self, key: str):
        return await self.redis_cache.get(key)

    # 특정 키에 만료 시간 지정
    async def expire(self, key: str, timeout: int):
        return await self.redis_cache.expire(key, timeout)

    # redis의 hash 타입에 값 지정
    async def hset(self, name: str, key: str, value: str):
        return await self.redis_cache.hset(name, key, value)

    # hset으로 저장한 hash 값에서 특정 필드 값 조회
    async def hget(self, name: str, key: str):
        return await self.redis_cache.hget(name, key)

    # hash 내 특정 필드 삭제
    async def hdel(self, name: str, key: str):
        return await self.redis_cache.hdel(name, key)

    # 해당 key 전체 삭제
    async def delete(self, name: str):
        return await self.redis_cache.delete(name)

    # 존재 여부
    async def exists(self, key: str) -> bool:
        result = await self.redis_cache.exists(key)
        return result > 0

    # Redis 연결 종료
    async def close(self):
        await self.redis_cache.close()


redis_cache = RedisCache()
