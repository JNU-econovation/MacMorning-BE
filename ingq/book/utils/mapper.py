from typing import Optional

from book.domain.book import Book as BookVO
from book.domain.character import Character as CharacterVO
from book.dto.schemas import (
    BookDetailItem,
    BookItem,
    CharacterResponse,
    CreateBookResponse,
)
from book.infra.db_models.book import Book
from core.setting.load_env import CLOUDFRONT_DOMAIN


class BookMapper:
    @staticmethod
    def book_to_create_book_response(book: BookVO) -> CreateBookResponse:
        _character = CharacterResponse(
            grammatical_person=book.character.grammatical_person,
            historical_background=book.character.historical_background,
            name=book.character.name,
            age=book.character.age,
            gender=book.character.gender,
            characteristic=book.character.characteristic,
        )
        return CreateBookResponse(
            id=book.id,
            user_id=book.user_id,
            genre=book.genre,
            gamemode=book.gamemode,
            character=_character,
            title=book.title,
            title_img=book.title_img,
            background=book.background,
            is_in_progress=book.is_in_progress,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    # Infra 계층에서 사용하는 메서드
    @staticmethod
    def bookvo_to_book(book: BookVO) -> Book:
        return Book(
            user_id=book.user_id,
            genre=book.genre,
            gamemode=book.gamemode,
            character=book.character.__dict__,
            title=book.title,
            title_img=book.title_img,
            background=book.background,
            is_in_progress=book.is_in_progress,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    @staticmethod
    def book_to_bookvo(book: Book) -> BookVO:
        return BookVO(
            id=book.id,
            user_id=book.user_id,
            genre=book.genre,
            gamemode=book.gamemode,
            character=CharacterVO(**book.character),
            title=book.title,
            title_img=book.title_img,
            background=book.background,
            is_in_progress=book.is_in_progress,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    @staticmethod
    def to_book_items_in_get_all_books_with_user_id(
        books_with_username_and_is_bookmarked: list[tuple[Book, str, bool]],
    ) -> list[BookItem]:
        result = []
        for (
            book,
            username,
            is_bookmarked,
            total_page,
        ) in books_with_username_and_is_bookmarked:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    is_bookmarked=is_bookmarked,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def to_book_items_in_get_all_books(
        books_with_username: list[tuple[Book, str]],
    ) -> list[BookItem]:
        result = []
        for book, username, total_page in books_with_username:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def to_book_items_in_get_mybooks(
        books_with_username_and_is_bookmarked: list[tuple[Book, str, bool]],
    ) -> list[BookItem]:
        result = []
        for (
            book,
            username,
            is_bookmarked,
            total_page,
        ) in books_with_username_and_is_bookmarked:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    is_bookmarked=is_bookmarked,
                    is_in_progress=book.is_in_progress,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def to_book_items_in_get_bookmarked_books(
        books_with_username: list[tuple[Book, str]],
    ) -> list[BookItem]:
        result = []
        for book, username, total_page in books_with_username:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    is_bookmarked=True,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def to_book_items_in_get_best_books_with_user_id(
        books_with_username_and_is_bookmarked_and_bookmark_count: list[
            tuple[Book, str, bool, int]
        ],
    ) -> list[BookItem]:
        result = []
        for (
            book,
            username,
            is_bookmarked,
            bookmark_count,
            total_page,
        ) in books_with_username_and_is_bookmarked_and_bookmark_count:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    is_bookmarked=is_bookmarked,
                    bookmark_count=bookmark_count,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def to_book_items_in_get_best_books(
        books_with_username_and_bookmark_count: list[tuple[Book, str, int]],
    ) -> list[BookItem]:
        result = []
        for (
            book,
            username,
            bookmark_count,
            total_page,
        ) in books_with_username_and_bookmark_count:
            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
                    title=book.title,
                    author=username,
                    background=book.background,
                    bookmark_count=bookmark_count,
                    total_page=total_page,
                )
            )
        return result

    @staticmethod
    def book_to_book_detail_item(
        book: Book, username: str, is_bookmarked: Optional[bool]
    ) -> BookDetailItem:
        return BookDetailItem(
            book_id=book.id,
            title_img_url=CLOUDFRONT_DOMAIN + book.title_img,
            title=book.title,
            author=username,
            background=book.background,
            is_bookmarked=is_bookmarked,
            character=CharacterResponse(
                grammatical_person=book.character.grammatical_person,
                historical_background=book.character.historical_background,
                name=book.character.name,
                age=book.character.age,
                gender=book.character.gender,
                characteristic=book.character.characteristic,
            ),
            genre=book.genre,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
