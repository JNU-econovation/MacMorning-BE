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
from book.infra.pagination.cursor import (
    validate_and_get_cursor,
    BookmarkCountCursor,
    Cursor,
    CreatedAtCursor,
    UpdatedAtCursor,
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
        decoded_cursor = (
            validate_and_get_cursor(cursor, order_strategy) if cursor else None
        )
        with SessionLocal() as db:
            query = build_query_base(db)
            total_count = query.count()

            query = get_ordered_query(query, order_strategy, decoded_cursor)

            # books_with_username: tuple (Book, username)
            books_with_username = query.limit(limit + 1).all()
            has_next = len(books_with_username) > limit
            books_to_return = books_with_username[:limit]

            book_items = get_book_items(books_to_return)

            next_cursor = get_next_cursor(books_to_return, order_strategy, has_next)
            page_info = PageInfo(has_next=has_next, total_count=total_count)

            return PaginatedBookItem(
                books=book_items, next_cursor=next_cursor, page_info=page_info
            )


def build_query_base(db, user_id=None, progress=None):
    """
    기본적인 Book과 User 조인 쿼리를 생성하는 함수

    Args
        db: Session - db 세션 객체
        user_id: Optional[int] - 특정 사용자의 책만 필터링할 사용자 ID
        progress: Optional[bool] - 진행 중 여부로 필터링 (True: 진행 중, False: 완료, None: 전부)

    Returns
        query: 기본 필터가 적용된 SQLAlchemy 쿼리 객체
    """
    query = db.query(Book, User.username).join(User, Book.user_id == User.id)

    if user_id is not None:
        query = query.filter(Book.user_id == user_id)

    if progress in [True, False]:
        query = query.filter(Book.is_in_progress == progress)

    return query


def get_ordered_query(query, order_strategy, cursor=None):
    """
    정렬 전략 및 커서 조건을 적용한 쿼리 반환

    Args
        query: Query - 정렬할 SQLAlchemy 쿼리 객체
        order_strategy: OrderStrategy - 정렬 전략 열거형 값
            - CREATED_AT_DESC - 생성일 기준 내림차순
            - CREATED_AT_ASC - 생성일 기준 오름차순
            - UPDATED_AT_DESC - 수정일 기준 내림차순
            - UPDATED_AT_ASC - 생성일 기준 오름차순
            - BOOKMARK_COUNT_DESC - 북마크 개수 기준 내림차순
            - BOOKMARK_COUNT_ASC - 북마크 개수 기준 오름차순
        cursor:

    Return
        query: 정렬 및 커서 필터가 적용된 SQLAlchemy 쿼리 객체
    """
    if order_strategy == OrderStrategy.CREATED_AT_DESC:
        query = query.order_by(desc(Book.created_at), desc(Book.id))
        if cursor:
            query = query.filter(
                (Book.created_at < cursor.created_at)
                | ((Book.created_at == cursor.created_at) & (Book.id < cursor.book_id))
            )
    elif order_strategy == OrderStrategy.CREATED_AT_ASC:
        query = query.order_by(asc(Book.created_at), asc(Book.id))
        if cursor:
            query = query.filter(
                (Book.created_at > cursor.created_at)
                | ((Book.created_at == cursor.created_at) & (Book.id > cursor.book_id))
            )
    elif order_strategy == OrderStrategy.UPDATED_AT_DESC:
        query = query.order_by(desc(Book.updated_at), desc(Book.id))
        if cursor:
            query = query.filter(
                (Book.updated_at < cursor.updated_at)
                | ((Book.updated_at == cursor.updated_at) & (Book.id < cursor.book_id))
            )
    elif order_strategy == OrderStrategy.UPDATED_AT_ASC:
        query = query.order_by(asc(Book.updated_at), asc(Book.id))
        if cursor:
            query = query.filter(
                (Book.updated_at > cursor.updated_at)
                | ((Book.updated_at == cursor.updated_at) & (Book.id > cursor.book_id))
            )
    elif order_strategy == OrderStrategy.BOOKMARK_COUNT_DESC:
        raise NotImplementedError("bookmark_count_desc는 구현중입니다.")
    elif order_strategy == OrderStrategy.BOOKMARK_COUNT_ASC:
        raise NotImplementedError("bookmark_count_desc는 구현중입니다.")

    return query


def get_book_items(books_with_username):
    """
    (Book, username) 튜플 리스트를 BookItem DTO로 변환하는 함수

    Args
        books_with_username: list[tuple] - (Book, username) 튜플 리스트

    Returns
        BookItem: 객체 리스트
    """
    return [
        BookItem(
            id=book.id,
            title_img_url="https://placehold.co/400",
            title=book.title,
            author=username,
            background=book.background,
        )
        for book, username in books_with_username
    ]


def get_next_cursor(books_to_return, order_strategy, has_next):
    """
    CreatedAtCursor, UpdatedAtCursor, BookmarkCountCursor를 인코딩 하여 반환
    다음 값(책)이 없는 경우 None 반환

    Args
        books_to_return: list[tuple] - (Book, username) 튜플 리스트
        order_strategy: OrderStrategy
        has_next: bool - 다음 Item이 있는지 판단

    Returns
        Encoding된 Cursor 값
    """
    if not has_next or not books_to_return:
        return None

    last_book = books_to_return[-1][0]

    cursor_config = {
        OrderStrategy.CREATED_AT_ASC: (CreatedAtCursor, "created_at"),
        OrderStrategy.CREATED_AT_DESC: (CreatedAtCursor, "created_at"),
        OrderStrategy.UPDATED_AT_ASC: (UpdatedAtCursor, "updated_at"),
        OrderStrategy.UPDATED_AT_DESC: (UpdatedAtCursor, "updated_at"),
        OrderStrategy.BOOKMARK_COUNT_ASC: (BookmarkCountCursor, "bookmark_count"),
        OrderStrategy.BOOKMARK_COUNT_DESC: (BookmarkCountCursor, "bookmark_count"),
    }

    cursor_class, field_name = cursor_config[order_strategy]

    field_value = getattr(last_book, field_name)

    cursor_params = {field_name: field_value, "book_id": last_book.id}
    cursor_instance = cursor_class(**cursor_params)

    return Cursor.encode(cursor_instance)
