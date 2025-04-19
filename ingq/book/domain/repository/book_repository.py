from abc import ABCMeta, abstractmethod
from book.domain.book import Book


class BookRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, book: Book) -> Book:
        raise NotImplementedError
