from datetime import datetime, timezone

from sqlalchemy.orm import Session

from choice.application.choice_service import ChoiceService
from illust.application.illust_service import IllustService
from story.domain.repository.story_repository import StoryRepository
from story.domain.story import Story
from story.dto.schemas import (
    CreateStoryResponse,
    CreateStoryWithIllustAndChoiceRequest,
    CreateStoryWithIllustAndChoiceResponse,
)


class StoryService:
    def __init__(
        self,
        story_repository: StoryRepository,
        illust_service: IllustService,
        choice_service: ChoiceService,
    ):
        self.story_repository = story_repository
        self.illust_service = illust_service
        self.choice_service = choice_service

    def create_story_with_illust_and_choice(
        self,
        user_id: str,
        create_story_with_illust_and_choice_request: CreateStoryWithIllustAndChoiceRequest,
        session: Session,
    ) -> CreateStoryWithIllustAndChoiceResponse:
        now = datetime.now(timezone.utc)
        with session.begin():
            story = Story(
                id=None,
                book_id=create_story_with_illust_and_choice_request.story.book_id,
                page_number=create_story_with_illust_and_choice_request.story.page_number,
                story_text=create_story_with_illust_and_choice_request.story.story_text,
                created_at=now,
                updated_at=now,
            )
            saved_story = self.story_repository.save(story, db=session)

            saved_illust = None
            saved_choice = None

            if create_story_with_illust_and_choice_request.illust:
                saved_illust = self.illust_service.create_illust(
                    saved_story.id,
                    create_story_with_illust_and_choice_request.illust,
                    session,
                )

            if create_story_with_illust_and_choice_request.choice:
                saved_choice = self.choice_service.create_choice(
                    saved_story.id,
                    create_story_with_illust_and_choice_request.choice,
                    session,
                )

        return CreateStoryWithIllustAndChoiceResponse(
            story=CreateStoryResponse(
                story_id=saved_story.id,
                book_id=saved_story.book_id,
                page_number=saved_story.page_number,
                story_text=saved_story.story_text,
                created_at=saved_story.created_at,
                updated_at=saved_story.updated_at,
            ),
            illust=saved_illust,
            choice=saved_choice,
        )
