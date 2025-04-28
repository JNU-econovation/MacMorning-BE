from typing import Optional

from book.domain.book import Book as BookVO
from book.domain.repository.book_repository import BookRepository
from book.dto.schemas import (
    PageInfo,
    PaginatedBookItem,
)
from book.infra.db_models.book import Book
from book.infra.pagination.cursor import (
    create_next_bookmark_cursor,
    create_next_cursor,
    get_bookmark_cursor,
    validate_and_get_cursor,
)
from book.infra.pagination.order_strategy import OrderStrategy
from book.infra.repository.book_query_builder import BookQueryBuilder
from book.utils.mapper import BookMapper
from db.database import SessionLocal


class MysqlBookRepository(BookRepository):
    def save(self, book: BookVO) -> BookVO:
        with SessionLocal() as db:
            try:
                new_book = BookMapper.bookvo_to_book(book)
                db.add(new_book)
                db.commit()
            except Exception as exc:
                db.rollback()
                raise exc

            return BookMapper.book_to_bookvo(new_book)

    def find_by_id(self, book_id: int) -> Optional[BookVO]:
        with SessionLocal() as db:
            book = db.query(Book).filter(Book.id == book_id).first()

            if not book:
                return None

            return BookMapper.book_to_bookvo(book)

    def get_all_books(
        self,
        user_id: Optional[str],
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        decoded_cursor = (
            validate_and_get_cursor(cursor, order_strategy) if cursor else None
        )
        with SessionLocal() as db:
            query = BookQueryBuilder.build_all_books_query(db, user_id)
            total_count = query.count()

            query = BookQueryBuilder.apply_ordering_and_filtering(
                query, order_strategy, decoded_cursor
            )

            # books의 query 반환 결과 두 가지
            books = query.limit(limit + 1).all()
            has_next = len(books) > limit
            books_to_return = books[:limit]

            if user_id:  # books: tuple[Book, str, bool] (Book, username, is_bookmarked)
                book_items = BookMapper.to_book_items_in_get_all_books_with_user_id(
                    books_to_return
                )
                books = [book for book, _, _ in books_to_return]
            else:  # books: tuple[Book, str] (Book, username)
                book_items = BookMapper.to_book_items_in_get_all_books(books_to_return)
                books = [book for book, _ in books_to_return]

            next_cursor = create_next_cursor(books, order_strategy, has_next)
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )

    def get_mybooks(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
        progress: Optional[bool],
    ) -> PaginatedBookItem:
        decoded_cursor = (
            validate_and_get_cursor(cursor, order_strategy) if cursor else None
        )
        with SessionLocal() as db:
            query = BookQueryBuilder.build_mybooks_query(db, user_id, progress)
            total_count = query.count()

            query = BookQueryBuilder.apply_ordering_and_filtering(
                query, order_strategy, decoded_cursor
            )

            # books: tuple[Book, str, bool] (Book, username, is_bookmarked)
            books = query.limit(limit + 1).all()
            has_next = len(books) > limit
            books_to_return = books[:limit]

            book_items = BookMapper.to_book_items_in_get_mybooks(books_to_return)

            books = [book for book, _, _ in books_to_return]
            next_cursor = create_next_cursor(books, order_strategy, has_next)
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )

    def get_bookmarked_books(
        self,
        user_id: str,
        limit: int,
        order_strategy: OrderStrategy,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        decoded_cursor = (
            validate_and_get_cursor(cursor, order_strategy) if cursor else None
        )
        with SessionLocal() as db:
            query = BookQueryBuilder.build_bookmarked_query(db, user_id)
            total_count = query.count()

            query = BookQueryBuilder.apply_ordering_and_filtering(
                query, order_strategy, decoded_cursor
            )

            # books: tuple[Book, str] (Book, username)
            books = query.limit(limit + 1).all()
            has_next = len(books) > limit
            books_to_return = books[:limit]

            book_items = BookMapper.to_book_items_in_get_bookmarked_books(
                books_to_return
            )

            books = [book for book, _ in books_to_return]
            next_cursor = create_next_cursor(books, order_strategy, has_next)
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )

    def get_best_books(
        self,
        user_id: Optional[str],
        limit: int,
        cursor: Optional[str],
    ) -> PaginatedBookItem:
        decoded_cursor = get_bookmark_cursor(cursor) if cursor else None
        with SessionLocal() as db:
            query = BookQueryBuilder.build_books_by_bookmark_count_query(db, user_id)
            total_count = query.count()

            query = BookQueryBuilder.apply_ordering_and_filtering_with_bookmark_count(
                query, decoded_cursor
            )

            books = query.limit(limit + 1).all()
            has_next = len(books) > limit
            books_to_return = books[:limit]

            if user_id:  # books: tuple[Book, str, bool, int] (Book, username, is_bookmarked, bookmark_count)
                book_items = BookMapper.to_book_items_in_get_best_books_with_user_id(
                    books_to_return
                )

                books_with_bookmark_count = [
                    (book, bookmark_count)
                    for book, _, _, bookmark_count in books_to_return
                ]
            else:  # books: tuple[Book, str, int] (Book, username, bookmark_count)
                book_items = BookMapper.to_book_items_in_get_best_books(books_to_return)
                books_with_bookmark_count = [
                    (book, bookmark_count)
                    for book, _, bookmark_count in books_to_return
                ]

            next_cursor = create_next_bookmark_cursor(
                books_with_bookmark_count, has_next
            )
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )
