from book.domain.book import Book
from book.domain.repository.book_repository import BookRepository
from book.exception.book_exception import BookNotFoundException


class BookReader:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get_book_by_id_or_throw(self, book_id: int) -> Book:
        book = self.book_repository.find_by_id(book_id)
        if not book:
            raise BookNotFoundException()
        return book
