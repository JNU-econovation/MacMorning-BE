from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from book.domain.book import Book
from book.domain.repository.book_repository import BookRepository
from book.dto.schemas import (
    CreateBookRequest,
    CreateBookResponse,
    PaginatedBookItem,
)
from book.exception.book_exception import BookNotFoundException
from book.infra.pagination.order_strategy import OrderStrategy
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

    def get_all_books(
        self,
        user_id: Optional[str],
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str] = None,
    ) -> PaginatedBookItem:
        return self.book_repository.get_all_books(
            user_id, limit=limit, order_strategy=order_strategy, cursor=cursor
        )

    def get_mybooks(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str] = None,
        progress: Optional[bool] = None,
    ) -> PaginatedBookItem:
        return self.book_repository.get_mybooks(
            user_id,
            limit=limit,
            order_strategy=order_strategy,
            cursor=cursor,
            progress=progress,
        )

    def get_bookmarked_books(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str] = None,
    ) -> PaginatedBookItem:
        return self.book_repository.get_bookmarked_books(
            user_id,
            limit=limit,
            order_strategy=order_strategy,
            cursor=cursor,
        )

    def get_best_books(
        self,
        user_id: Optional[str],
        limit: int,
        cursor: Optional[str] = None,
    ) -> PaginatedBookItem:
        return self.book_repository.get_best_books(
            user_id,
            limit=limit,
            cursor=cursor,
        )

    def get_book_by_id_or_throw(self, book_id: int) -> Book:
        book = self.book_repository.find_by_id(book_id)
        if not book:
            raise BookNotFoundException()
        return book

    def set_is_in_progress_to_false(self, book: Book, db: Session) -> Book:
        now = datetime.now(timezone.utc)
        book.updated_at = now
        book.set_is_in_progress_to_false()
        return self.book_repository.update_is_in_progress_to_false(book, db)
