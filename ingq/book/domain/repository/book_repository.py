from abc import ABCMeta, abstractmethod
from typing import Optional

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
