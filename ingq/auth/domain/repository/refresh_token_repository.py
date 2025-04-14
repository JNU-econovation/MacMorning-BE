from abc import ABC, abstractmethod


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def save(self, user_id: str, token: str, expire: int):
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: str):
        raise NotImplementedError

    @abstractmethod
    async def exists_by_user_id(self, user_id: str):
        raise NotImplementedError
