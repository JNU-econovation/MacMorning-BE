from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Story:
    id: Optional[int]
    book_id: int
    page_number: int
    story_text: str
    created_at: datetime
    updated_at: datetime
