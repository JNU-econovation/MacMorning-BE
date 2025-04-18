from dataclasses import dataclass
from datetime import datetime

from book.domain.character import Character


@dataclass
class Book:
    id: int
    user_id: str
    genre: list[str]
    gamemode: bool
    character: Character
    title: str
    background: str
    is_storage: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        unique_genres = list(dict.fromkeys(self.genre))
        self.genre = unique_genres[:3]
