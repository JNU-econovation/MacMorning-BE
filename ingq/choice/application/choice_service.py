from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from choice.domain.choice import Choice
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.dto.schemas import ChoiceItem, CreateChoiceRequest, CreateChoiceResponse
from choice.utils.mapper import ChoiceMapper


class ChoiceService:
    def __init__(self, choice_repository: ChoiceRepository):
        self.choice_repository = choice_repository

    def create_choice(
        self,
        story_id: int,
        create_choice_request: CreateChoiceRequest,
        session: Session,
    ) -> CreateChoiceResponse:
        now = datetime.now(timezone.utc)
        choice = Choice.create_choice_request_to_choice(
            story_id, create_choice_request, now
        )

        saved_choice = self.choice_repository.save(choice, db=session)

        return ChoiceMapper.to_create_choice_response(saved_choice)

    def get_choice_item_by_story_id(
        self, story_id: int, session: Session
    ) -> Optional[ChoiceItem]:
        choice = self.choice_repository.find_by_story_id(story_id, db=session)

        if not choice:
            return None

        return ChoiceMapper.choicevo_to_choice_item(choice)
