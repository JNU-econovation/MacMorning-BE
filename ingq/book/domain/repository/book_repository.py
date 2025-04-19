from abc import ABCMeta, abstractmethod
from typing import Optional, Any
from book.domain.book import Book
from book.infra.pagination.order_strategy import OrderStrategy
from book.dto.schemas import PaginatedBookItem


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
        cursor: Optional[Any],
    ) -> PaginatedBookItem:
        raise NotImplementedError
