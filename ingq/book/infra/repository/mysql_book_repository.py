from typing import Optional

from sqlalchemy.orm import Session

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
from bookmark.infra.db_models.bookmark import Bookmark
from db.database import SessionLocal
from story.infra.db_models.story import Story


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

    def update_is_in_progress_to_false(self, book: BookVO) -> BookVO:
        with SessionLocal() as db:
            existing_book = db.query(Book).filter(Book.id == book.id).first()
            existing_book.is_in_progress = book.is_in_progress
            existing_book.updated_at = book.updated_at
            db.commit()
            return BookMapper.book_to_bookvo(existing_book)

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

            if user_id:  # books: tuple[Book, str, bool]
                books_with_total_page = []
                for book, username, is_bookmarked in books_to_return:
                    total_page = self.get_total_page(book.id, db)
                    books_with_total_page.append(
                        (book, username, is_bookmarked, total_page)
                    )

                book_items = BookMapper.to_book_items_in_get_all_books_with_user_id(
                    books_with_total_page
                )

                books = [book for book, _, _, _ in books_with_total_page]

            else:  # books: tuple[Book, str]
                books_with_total_page = []
                for book, username in books_to_return:
                    total_page = self.get_total_page(book.id, db)
                    books_with_total_page.append((book, username, total_page))

                book_items = BookMapper.to_book_items_in_get_all_books(
                    books_with_total_page
                )

                books = [book for book, _, _ in books_with_total_page]

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

            books_with_total_page = []
            for book, username, is_bookmarked in books_to_return:
                total_page = self.get_total_page(book.id, db)
                books_with_total_page.append(
                    (book, username, is_bookmarked, total_page)
                )

            book_items = BookMapper.to_book_items_in_get_mybooks(books_with_total_page)

            books = [book for book, _, _, _ in books_with_total_page]

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

            books = query.limit(limit + 1).all()
            has_next = len(books) > limit
            books_to_return = books[:limit]

            books_with_total_page = []
            for book, username in books_to_return:
                total_page = self.get_total_page(book.id, db)
                books_with_total_page.append((book, username, total_page))

            book_items = BookMapper.to_book_items_in_get_bookmarked_books(
                books_with_total_page
            )

            books = [book for book, _, _ in books_with_total_page]
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

            if user_id:  # books: tuple[Book, str, bool, int]
                books_with_total_page = []
                for book, username, is_bookmarked, bookmark_count in books_to_return:
                    total_page = self.get_total_page(book.id, db)
                    books_with_total_page.append(
                        (book, username, is_bookmarked, bookmark_count, total_page)
                    )

                book_items = BookMapper.to_book_items_in_get_best_books_with_user_id(
                    books_with_total_page
                )

                books_with_bookmark_count = [
                    (book, bookmark_count)
                    for book, _, _, bookmark_count, _ in books_with_total_page
                ]
            else:  # books: tuple[Book, str, int]
                books_with_total_page = []
                for book, username, bookmark_count in books_to_return:
                    total_page = self.get_total_page(book.id, db)
                    books_with_total_page.append(
                        (book, username, bookmark_count, total_page)
                    )

                book_items = BookMapper.to_book_items_in_get_best_books(
                    books_with_total_page
                )

                books_with_bookmark_count = [
                    (book, bookmark_count)
                    for book, _, bookmark_count, _ in books_with_total_page
                ]

            next_cursor = create_next_bookmark_cursor(
                books_with_bookmark_count, has_next
            )
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )

    def is_bookmarked(self, user_id: Optional[str], book_id: int) -> Optional[bool]:
        if user_id is None:
            return None

        with SessionLocal() as db:
            bookmark = (
                db.query(Bookmark)
                .filter(Bookmark.user_id == user_id, Bookmark.book_id == book_id)
                .first()
            )

            return bookmark is not None

    def update_title_image(self, book: Book) -> None:
        with SessionLocal() as db:
            try:
                existing_book = db.query(Book).filter(Book.id == book.id).first()
                existing_book.title_img = book.title_img
                db.commit()
            except Exception as exc:
                db.rollback()
                raise exc

    def get_total_page(self, book_id: int, db: Session) -> int:
        return db.query(Story).filter(Story.book_id == book_id).count()
