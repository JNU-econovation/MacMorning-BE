from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from book.application.book_reader import BookReader
from illust.domain.illust import Illust
from illust.domain.repository.illust_repository import IllustRepository
from illust.dto.schemas import (
    CreateIllustRequest,
    CreateIllustResponse,
    IllustItem,
    IllustItemList,
)
from illust.utils.mapper import IllustMapper
from story.exception.story_exception import InvalidUserAccessException


class IllustService:
    def __init__(
        self,
        illust_repository: IllustRepository,
        book_reader: BookReader,
    ):
        self.illust_repository = illust_repository
        self.book_reader = book_reader

    def create_illust(
        self,
        story_id: int,
        create_illust_request: CreateIllustRequest,
        session: Session,
    ) -> CreateIllustResponse:
        now = datetime.now(timezone.utc)
        illust = Illust.create_illust_request_to_illust(
            story_id, create_illust_request, now
        )
        saved_illust = self.illust_repository.save(illust, db=session)

        return IllustMapper.to_create_illust_response(saved_illust)

    def get_illust_item_by_story_id(
        self, story_id: int, session: Session
    ) -> Optional[IllustItem]:
        illust = self.illust_repository.find_by_story_id(story_id, db=session)

        if not illust:
            return None

        return IllustMapper.illustvo_to_illust_item(illust)

    def get_illust_item_list_by_book(
        self,
        user_id: str,
        book_id: int,
    ) -> IllustItemList:
        book = self.book_reader.get_book_by_id_or_throw(book_id)

        if book.user_id != user_id:
            raise InvalidUserAccessException()

        illusts = self.illust_repository.find_all_by_book_id(book.id)
        return IllustMapper.illustsvo_to_illust_item_list(illusts)
