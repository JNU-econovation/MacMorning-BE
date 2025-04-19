from datetime import datetime, timezone
from book.domain.book import Book
from book.domain.repository.book_repository import BookRepository

from book.dto.schemas import CreateBookRequest, CreateBookResponse

from book.utils.mapper import BookMapper


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book(
        self, user_id: str, create_book_request: CreateBookRequest
    ) -> CreateBookResponse:
        now = datetime.now(timezone.utc)

        book = Book.create_book_request_to_book(user_id, create_book_request, now)

        saved_book = self.book_repository.save(book)

        return BookMapper.book_to_create_book_response(saved_book)
