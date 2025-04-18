from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from typing import Optional

from book.domain.character import Character

from book.dto.schemas import CreateBookRequest


@dataclass
class Book:
    id: Optional[int]
    user_id: str
    genre: list[str]
    gamemode: bool
    character: Character
    title: str
    background: str
    is_storage: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_book_request_to_book(
        cls, user_id: str, request: CreateBookRequest, now: datetime
    ) -> Book:
        _character = Character(
            name=request.character.name,
            age=request.character.age,
            gender=request.character.gender,
            characteristic=request.character.characteristic,
        )
        return cls(
            id=None,
            user_id=user_id,
            genre=request.genre,
            gamemode=request.gamemode,
            character=_character,
            title=request.title,
            background=request.background,
            is_storage=request.is_storage,
            created_at=now,
            updated_at=now,
        )
