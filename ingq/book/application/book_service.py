from datetime import datetime
from book.domain.book import Book
from book.domain.repository.book_repository import BookRepository

from book.dto.schemas import CreateBookRequest, CreateBookResponse

from book.utils.mapper import BookMapper


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book(
        self, user_id: str, createBookRequest: CreateBookRequest
    ) -> CreateBookResponse:
        now = datetime.now()

        book = Book.create_book_request_to_book(user_id, createBookRequest, now)

        saved_book = self.book_repository.save(book)

        return BookMapper.book_to_create_book_response(saved_book)
