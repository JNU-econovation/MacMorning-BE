from datetime import datetime, timezone

from sqlalchemy.orm import Session

from choice.domain.choice import Choice
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.dto.schemas import CreateChoiceRequest, CreateChoiceResponse
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
