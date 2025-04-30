from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from book.application.book_service import BookService
from choice.application.choice_service import ChoiceService
from illust.application.illust_service import IllustService
from story.domain.repository.story_repository import StoryRepository
from story.domain.story import Story
from story.dto.schemas import (
    CreateStoryResponse,
    CreateStoryWithIllustAndChoiceRequest,
    CreateStoryWithIllustAndChoiceResponse,
)
from story.exception.story_exception import (
    DuplicatePageNumberException,
    InvalidBookProgressException,
    InvalidChoiceException,
    InvalidUserAccessException,
)


class StoryService:
    def __init__(
        self,
        story_repository: StoryRepository,
        illust_service: IllustService,
        choice_service: ChoiceService,
        book_service: BookService,
    ):
        self.story_repository = story_repository
        self.illust_service = illust_service
        self.choice_service = choice_service
        self.book_service = book_service

    def create_story_with_illust_and_choice(
        self,
        user_id: str,
        book_id: int,
        create_story_with_illust_and_choice_request: CreateStoryWithIllustAndChoiceRequest,
        session: Session,
    ) -> CreateStoryWithIllustAndChoiceResponse:
        now = datetime.now(timezone.utc)
        with session.begin():
            story_request = create_story_with_illust_and_choice_request.story
            illust_request = create_story_with_illust_and_choice_request.illust
            choice_request = create_story_with_illust_and_choice_request.choice

            book = self.book_service.get_book_by_id_or_throw(book_id)

            if book.user_id != user_id:
                raise InvalidUserAccessException()

            existing_story = self.get_story_by_book_id_and_page_number(
                book_id, story_request.page_number
            )
            if existing_story:
                raise DuplicatePageNumberException()

            if not book.is_in_progress:
                raise InvalidBookProgressException()

            story = Story(
                id=None,
                book_id=book_id,
                page_number=story_request.page_number,
                story_text=story_request.story_text,
                created_at=now,
                updated_at=now,
            )
            saved_story = self.story_repository.save(story, db=session)

            saved_illust = None
            saved_choice = None

            if illust_request:
                saved_illust = self.illust_service.create_illust(
                    saved_story.id,
                    illust_request,
                    session,
                )

            if choice_request:
                if book.gamemode:
                    pass
                else:
                    if not choice_request.is_success:
                        raise InvalidChoiceException()

                saved_choice = self.choice_service.create_choice(
                    saved_story.id,
                    choice_request,
                    session,
                )
            else:
                book.set_is_in_progress_to_false()

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

    def get_story_by_book_id_and_page_number(
        self, book_id: int, page_number: int
    ) -> Optional[Story]:
        return self.story_repository.find_by_book_id_and_page_number(
            book_id, page_number
        )
