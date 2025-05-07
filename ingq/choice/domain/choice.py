from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from choice.dto.schemas import CreateChoiceRequest


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

    @classmethod
    def create_choice_request_to_choice(
        cls, story_id: int, request: CreateChoiceRequest, now: datetime
    ) -> Choice:
        return cls(
            id=None,
            story_id=story_id,
            first_choice=request.first_choice,
            second_choice=request.second_choice,
            third_choice=request.third_choice,
            my_choice=request.my_choice,
            is_success=request.is_success,
            created_at=now,
            updated_at=now,
        )
