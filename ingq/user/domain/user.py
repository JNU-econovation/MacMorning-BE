from dataclasses import dataclass
from datetime import datetime

from user.domain.provider import Provider


@dataclass
class User:
    id: str  # PK - ULID
    email: str
    password: str  # 암호화
    nickname: str
    profile_image: str
    username: str
    phone_number: str  # 암호화
    provider: Provider
    created_at: datetime
    updated_at: datetime
