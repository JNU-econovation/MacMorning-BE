from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Bookmark:
    id: Optional[int]
    user_id: str
    book_id: int
    created_at: datetime
