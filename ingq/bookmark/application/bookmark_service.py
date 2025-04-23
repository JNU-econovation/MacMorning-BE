from datetime import datetime, timezone

from book.application.book_service import BookService
from bookmark.domain.bookmark import Bookmark
from bookmark.domain.repository.bookmark_repository import BookmarkRepository
from bookmark.dto.schemas import BookmarkRequest, BookmarkResponse

BOOKMARK_SUCCESS_MESSAGE = "북마크 성공"
BOOKMARK_CANCEL_MESSAGE = "북마크 취소"


class BookmarkService:
    def __init__(
        self,
        bookmark_repository: BookmarkRepository,
        book_service: BookService,
    ):
        self.bookmark_repository = bookmark_repository
        self.book_service = book_service

    def toggle_bookmark(
        self, user_id: str, bookmark_request: BookmarkRequest
    ) -> BookmarkResponse:
        book_id = bookmark_request.book_id
        self.book_service.get_book_by_id_or_throw(book_id)
        bookmark = self.bookmark_repository.find_by_user_id_and_book_id(
            user_id, book_id
        )
        now = datetime.now(timezone.utc)
        if bookmark:
            self.bookmark_repository.delete(bookmark)
            return BookmarkResponse(message=BOOKMARK_CANCEL_MESSAGE)
        else:
            new_bookmark = Bookmark(
                id=None, user_id=user_id, book_id=book_id, created_at=now
            )
            self.bookmark_repository.save(new_bookmark)
            return BookmarkResponse(message=BOOKMARK_SUCCESS_MESSAGE)
