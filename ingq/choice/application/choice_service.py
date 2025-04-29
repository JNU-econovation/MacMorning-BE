from datetime import datetime, timezone

from sqlalchemy.orm import Session

from choice.domain.choice import Choice
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.dto.schemas import CreateChoiceRequest, CreateChoiceResponse


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
        choice = Choice(
            id=None,
            story_id=story_id,
            first_choice=create_choice_request.first_choice,
            second_choice=create_choice_request.second_choice,
            third_choice=create_choice_request.third_choice,
            my_choice=create_choice_request.my_choice,
            is_success=create_choice_request.is_success,
            created_at=now,
            updated_at=now,
        )
        saved_choice = self.choice_repository.save(choice, db=session)

        return CreateChoiceResponse(
            choice_id=saved_choice.id,
            story_id=saved_choice.story_id,
            first_choice=saved_choice.first_choice,
            second_choice=saved_choice.second_choice,
            third_choice=saved_choice.third_choice,
            my_choice=saved_choice.my_choice,
            is_success=saved_choice.is_success,
            created_at=saved_choice.created_at,
            updated_at=saved_choice.updated_at,
        )
