from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Choice:
    id: Optional[int]
    story_id: int
    first_choice: str
    second_choice: str
    third_choice: Optional[str]
    my_choice: int
    is_success: bool
    created_at: datetime
    updated_at: datetime
