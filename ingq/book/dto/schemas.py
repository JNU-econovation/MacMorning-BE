from pydantic import BaseModel
from datetime import datetime


class CharacterRequest(BaseModel):
    name: str
    age: int
    gender: str
    characteristic: list[str]


class CharacterResponse(BaseModel):
    name: str
    age: int
    gender: str
    characteristic: list[str]


class CreateBookRequest(BaseModel):
    genre: list[str]
    gamemode: bool
    character: CharacterRequest
    title: str
    background: str
    is_storage: bool = True  # True (이야기 진행중)


# 논의 후 변경 예정
class CreateBookResponse(BaseModel):
    id: int
    user_id: str
    genre: list[str]
    gamemode: bool
    character: CharacterResponse
    title: str
    background: str
    is_storage: bool
    created_at: datetime
    updated_at: datetime
