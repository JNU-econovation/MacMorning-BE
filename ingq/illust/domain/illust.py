from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Illust:
    id: Optional[int]
    story_id: int
    image_url: str
    created_at: datetime
    updated_at: datetime
