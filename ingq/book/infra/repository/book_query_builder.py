from typing import Optional

from sqlalchemy import asc, desc
from sqlalchemy.orm import Query, Session

from book.infra.db_models.book import Book
from book.infra.pagination.cursor import (
    Cursor,
)
from book.infra.pagination.order_strategy import OrderStrategy
from bookmark.infra.db_models.bookmark import Bookmark
from user.infra.db_models.user import User


class BookQueryBuilder:
    @staticmethod
    def build_all_books_query(db: Session, user_id: Optional[str] = None) -> Query:
        if user_id:
            return (
                db.query(
                    Book, User.username, Bookmark.id.isnot(None).label("is_bookmarked")
                )
                .join(User, Book.user_id == User.id)
                .outerjoin(
                    Bookmark,
                    (Bookmark.book_id == Book.id) & (Bookmark.user_id == user_id),
                )
            )
        else:
            return db.query(Book, User.username).join(User, Book.user_id == User.id)

    @staticmethod
    def build_mybooks_query(
        db: Session, user_id: str, progress: Optional[bool] = None
    ) -> Query:
        query = (
            db.query(
                Book, User.username, Bookmark.id.isnot(None).label("is_bookmarked")
            )
            .join(User, Book.user_id == User.id)
            .outerjoin(
                Bookmark, (Bookmark.book_id == Book.id) & (Bookmark.user_id == user_id)
            )
            .filter(Book.user_id == user_id)
        )

        if progress in [True, False]:
            query = query.filter(Book.is_in_progress == progress)

        return query

    @staticmethod
    def build_bookmarked_query(db: Session, user_id: str) -> Query:
        return (
            db.query(Book, User.username)
            .join(Bookmark, Bookmark.book_id == Book.id)
            .join(User, Book.user_id == User.id)
            .filter(Bookmark.user_id == user_id)
        )

    @staticmethod
    def apply_ordering_and_filtering(
        query: Query, order_strategy: OrderStrategy, cursor: Optional[Cursor]
    ) -> Query:
        if order_strategy == OrderStrategy.CREATED_AT_DESC:
            query = query.order_by(desc(Book.created_at), desc(Book.id))
            if cursor:
                query = query.filter(
                    (Book.created_at < cursor.created_at)
                    | (
                        (Book.created_at == cursor.created_at)
                        & (Book.id < cursor.book_id)
                    )
                )
        elif order_strategy == OrderStrategy.CREATED_AT_ASC:
            query = query.order_by(asc(Book.created_at), asc(Book.id))
            if cursor:
                query = query.filter(
                    (Book.created_at > cursor.created_at)
                    | (
                        (Book.created_at == cursor.created_at)
                        & (Book.id > cursor.book_id)
                    )
                )
        elif order_strategy == OrderStrategy.UPDATED_AT_DESC:
            query = query.order_by(desc(Book.updated_at), desc(Book.id))
            if cursor:
                query = query.filter(
                    (Book.updated_at < cursor.updated_at)
                    | (
                        (Book.updated_at == cursor.updated_at)
                        & (Book.id < cursor.book_id)
                    )
                )
        elif order_strategy == OrderStrategy.UPDATED_AT_ASC:
            query = query.order_by(asc(Book.updated_at), asc(Book.id))
            if cursor:
                query = query.filter(
                    (Book.updated_at > cursor.updated_at)
                    | (
                        (Book.updated_at == cursor.updated_at)
                        & (Book.id > cursor.book_id)
                    )
                )
        elif order_strategy == OrderStrategy.BOOKMARK_COUNT_DESC:
            raise NotImplementedError("bookmark_count_desc는 구현중입니다.")
        elif order_strategy == OrderStrategy.BOOKMARK_COUNT_ASC:
            raise NotImplementedError("bookmark_count_asc는 구현중입니다.")

        return query
