from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from book.domain.book import Book
from book.dto.schemas import PaginatedBookItem
from book.infra.pagination.order_strategy import OrderStrategy


class BookRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, book: Book) -> Book:
        raise NotImplementedError

    @abstractmethod
    def get_all_books(
        self,
        user_id: Optional[str],
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        raise NotImplementedError

    @abstractmethod
    def get_mybooks(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
        progress: Optional[bool],
    ) -> PaginatedBookItem:
        raise NotImplementedError

    @abstractmethod
    def get_bookmarked_books(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        raise NotImplementedError

    @abstractmethod
    def get_best_books(
        self,
        user_id: Optional[str],
        limit: int,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, book_id: int) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def update_is_in_progress_to_false(self, book: Book, db: Session) -> Book:
        raise NotImplementedError
