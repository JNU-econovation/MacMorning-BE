from book.domain.book import Book
from book.dto.schemas import CreateBookResponse, CharacterResponse


class BookMapper:
    @staticmethod
    def book_to_create_book_response(book: Book) -> CreateBookResponse:
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
            is_storage=book.is_storage,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
