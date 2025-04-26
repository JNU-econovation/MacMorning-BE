from typing import Optional

from sqlalchemy import asc, desc, func, literal_column
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
    def build_books_by_bookmark_count_query(
        db: Session, user_id: Optional[str] = None
    ) -> Query:
        bookmark_count = (
            db.query(Bookmark.book_id, func.count(Bookmark.id).label("bookmark_count"))
            .group_by(Bookmark.book_id)
            .subquery()
        )

        if user_id:
            return (
                db.query(
                    Book,
                    User.username,
                    Bookmark.id.isnot(None).label("is_bookmarked"),
                    func.coalesce(bookmark_count.c.bookmark_count, 0).label(
                        "bookmark_count"
                    ),
                )
                .join(User, Book.user_id == User.id)
                .outerjoin(
                    Bookmark,
                    (Bookmark.book_id == Book.id) & (Bookmark.user_id == user_id),
                )
                .outerjoin(bookmark_count, Book.id == bookmark_count.c.book_id)
            )
        else:
            return (
                db.query(
                    Book,
                    User.username,
                    func.coalesce(bookmark_count.c.bookmark_count, 0).label(
                        "bookmark_count"
                    ),
                )
                .join(User, Book.user_id == User.id)
                .outerjoin(bookmark_count, Book.id == bookmark_count.c.book_id)
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

        return query

    @staticmethod
    def apply_ordering_and_filtering_with_bookmark_count(
        query: Query, cursor: Optional[Cursor]
    ) -> Query:
        query = query.order_by(desc(literal_column("bookmark_count")), desc(Book.id))
        print("book-query-builder-ordering:", query)
        if cursor:
            query = query.filter(
                (
                    func.coalesce(literal_column("bookmark_count"), 0)
                    < cursor.bookmark_count
                )
                | (
                    (
                        func.coalesce(literal_column("bookmark_count"), 0)
                        == cursor.bookmark_count
                    )
                    & (Book.id < cursor.book_id)
                )
            )
        return query
