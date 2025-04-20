from sqlalchemy import asc, desc

from book.domain.book import Book as BookVO
from book.domain.character import Character as CharacterVO
from book.domain.repository.book_repository import BookRepository
from book.dto.schemas import (
    BookItem,
    PageInfo,
    PaginatedBookItem,
)
from book.infra.db_models.book import Book
from book.infra.pagination.comparator.cursor_comparator_factory import (
    get_cursor_comparator,
)
from book.infra.pagination.order_strategy import OrderStrategy
from db.database import SessionLocal
from user.infra.db_models.user import User


class MysqlBookRepository(BookRepository):
    def save(self, book: BookVO) -> BookVO:
        with SessionLocal() as db:
            try:
                new_book = Book(
                    user_id=book.user_id,
                    genre=book.genre,
                    gamemode=book.gamemode,
                    character=book.character.__dict__,
                    title=book.title,
                    background=book.background,
                    is_in_progress=book.is_in_progress,
                    created_at=book.created_at,
                    updated_at=book.updated_at,
                )

                db.add(new_book)
                db.commit()
            except Exception as exc:
                db.rollback()
                raise exc

            return BookVO(
                id=new_book.id,
                user_id=new_book.user_id,
                genre=new_book.genre,
                gamemode=new_book.gamemode,
                character=CharacterVO(**new_book.character),
                title=new_book.title,
                background=new_book.background,
                is_in_progress=new_book.is_in_progress,
                created_at=new_book.created_at,
                updated_at=new_book.updated_at,
            )

    def get_all_books(
        self, user_id, limit, order_strategy, cursor
    ) -> PaginatedBookItem:
        comparator = get_cursor_comparator(order_strategy)

        with SessionLocal() as db:
            query = db.query(Book, User).join(User, Book.user_id == User.id)
            total_count = query.count()

            if order_strategy == OrderStrategy.CREATED_AT_DESC:
                query = query.order_by(desc(Book.created_at), desc(Book.id))
            elif order_strategy == OrderStrategy.CREATED_AT_ASC:
                query = query.order_by(asc(Book.created_at), asc(Book.id))
            elif order_strategy == OrderStrategy.UPDATED_AT_DESC:
                query = query.order_by(desc(Book.updated_at), desc(Book.id))
            elif order_strategy == OrderStrategy.UPDATED_AT_ASC:
                query = query.order_by(asc(Book.updated_at), asc(Book.id))
            # TODO: 북마크, 조회수 정렬 추가

            all_books = query.all()

            if cursor:
                all_books = [
                    (book, user)
                    for book, user in all_books
                    if comparator.is_after(book, cursor)
                ]

            sliced_books = all_books[: limit + 1]
            has_next = 1 if len(sliced_books) > limit else 0
            books = sliced_books[:limit]

            book_items = [
                BookItem(
                    id=book.id,
                    title_img_url="https://placehold.co/400",  # TODO: 이미지 URL 이야기에서 불러와 처리
                    title=book.title,
                    author=user.username,
                    background=book.background,
                    # TODO: 로그인 한 사용자의 경우 is_bookmarked 필드 추가 반환
                )
                for book, user in books
            ]

            next_cursor = None
            if books:
                last_book, _ = books[-1]
                next_cursor = comparator.extract_cursor(last_book)

            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )
