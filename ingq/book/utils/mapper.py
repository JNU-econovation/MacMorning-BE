from typing import Optional

from book.domain.book import Book as BookVO
from book.domain.character import Character as CharacterVO
from book.dto.schemas import BookItem, CharacterResponse, CreateBookResponse
from book.infra.db_models.book import Book


class BookMapper:
    @staticmethod
    def book_to_create_book_response(book: BookVO) -> CreateBookResponse:
        _character = CharacterResponse(
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
            background=book.background,
            is_in_progress=book.is_in_progress,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    @staticmethod
    def bookvo_to_book(book: BookVO) -> Book:
        return Book(
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

    @staticmethod
    def book_to_bookvo(book: Book) -> BookVO:
        return BookVO(
            id=book.id,
            user_id=book.user_id,
            genre=book.genre,
            gamemode=book.gamemode,
            character=CharacterVO(**book.character),
            title=book.title,
            background=book.background,
            is_in_progress=book.is_in_progress,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    @staticmethod
    def to_book_items(
        books_with_username: list[tuple[Book, str]],
        bookmarked_ids: Optional[set[int]] = None,
        force_bookmarked: Optional[bool] = None,
    ) -> list[BookItem]:
        result = []
        for book, username in books_with_username:
            if force_bookmarked is not None:
                is_bookmarked = force_bookmarked
            else:
                is_bookmarked = (
                    book.id in bookmarked_ids if bookmarked_ids is not None else False
                )

            result.append(
                BookItem(
                    book_id=book.id,
                    title_img_url="https://placehold.co/400",
                    title=book.title,
                    author=username,
                    background=book.background,
                    is_bookmarked=is_bookmarked,
                )
            )
        return result
