from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from story.dto.schemas import CreateStoryRequest


@dataclass
class Story:
    id: Optional[int]
    book_id: int
    page_number: int
    story_text: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_story_request_to_story(
        cls, book_id: int, request: CreateStoryRequest, now: datetime
    ) -> Story:
        return cls(
            id=None,
            book_id=book_id,
            page_number=request.page_number,
            story_text=request.story_text,
            created_at=now,
            updated_at=now,
        )
