from datetime import datetime, timezone

from typing import Optional, Any

from book.domain.book import Book
from book.domain.repository.book_repository import BookRepository

from book.dto.schemas import (
    CreateBookRequest,
    CreateBookResponse,
    PaginatedBookItem,
)

from book.utils.mapper import BookMapper

from book.infra.pagination.order_strategy import OrderStrategy
from book.infra.pagination.cursor import validate_and_get_cursor


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

    def get_all_books(
        self,
        user_id: Optional[str],
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[Any] = None,
    ) -> PaginatedBookItem:
        validated_cursor = validate_and_get_cursor(cursor, order_strategy)
        return self.book_repository.get_all_books(
            user_id, limit=limit, order_strategy=order_strategy, cursor=validated_cursor
        )
