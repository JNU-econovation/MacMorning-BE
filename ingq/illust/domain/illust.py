from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from illust.dto.schemas import CreateIllustRequest


@dataclass
class Illust:
    id: Optional[int]
    story_id: int
    image_url: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_illust_request_to_illust(
        cls, story_id: int, request: CreateIllustRequest, now: datetime
    ) -> Illust:
        return cls(
            id=None,
            story_id=story_id,
            image_url=request.image_url,
            created_at=now,
            updated_at=now,
        )
