from book.domain.book import Book as BookVO
from book.domain.character import Character as CharacterVO
from book.dto.schemas import CharacterResponse, CreateBookResponse
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
