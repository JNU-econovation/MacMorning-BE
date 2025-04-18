from db.database import SessionLocal

from book.domain.book import Book as BookVO
from book.domain.character import Character as CharacterVO
from book.domain.repository.book_repository import BookRepository

from book.infra.db_models.book import Book


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
