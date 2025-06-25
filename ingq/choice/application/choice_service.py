from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from book.application.book_reader import BookReader
from choice.domain.choice import Choice
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.dto.schemas import (
    ChoiceItem,
    CreateChoiceRequest,
    CreateChoiceResponse,
    LastChoiceItem,
    LastChoiceItemList,
    UpdateReasonRequest,
)
from choice.exception.choice_exception import ChoiceNotFoundException
from choice.utils.mapper import ChoiceMapper
from story.exception.story_exception import InvalidUserAccessException


class ChoiceService:
    def __init__(
        self,
        choice_repository: ChoiceRepository,
        book_reader: BookReader,
    ):
        self.choice_repository = choice_repository
        self.book_reader = book_reader

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

    def get_selected_choice_item_by_book_id(
        self,
        user_id: str,
        book_id: int,
    ) -> LastChoiceItemList:
        book = self.book_reader.get_book_by_id_or_throw(book_id)

        if book.user_id != user_id:
            raise InvalidUserAccessException()

        choices = self.choice_repository.find_all_by_book_id(book.id)

        last_choices = [
            ChoiceMapper.choicevo_to_last_choice_item(
                choice,
                [choice.first_choice, choice.second_choice, choice.third_choice][
                    choice.my_choice - 1
                ],
            )
            for choice in choices
        ]

        return LastChoiceItemList(choices=last_choices)

    def update_selected_choice(
        self,
        user_id: str,
        book_id: int,
        choice_id: int,
        reason: UpdateReasonRequest,
    ) -> LastChoiceItem:
        book = self.book_reader.get_book_by_id_or_throw(book_id)

        if book.user_id != user_id:
            raise InvalidUserAccessException()

        choice = self.choice_repository.find_by_id(choice_id)

        if choice is None:
            raise ChoiceNotFoundException()

        choice.reason = reason.reason
        updated_choice = self.choice_repository.save_reason(choice)
        content = [
            updated_choice.first_choice,
            updated_choice.second_choice,
            updated_choice.third_choice,
        ][updated_choice.my_choice - 1]

        return ChoiceMapper.choicevo_to_last_choice_item(updated_choice, content)
