from typing import Optional

from bookmark.domain.bookmark import Bookmark as BookmarkVO
from bookmark.domain.repository.bookmark_repository import BookmarkRepository
from bookmark.infra.db_models.bookmark import Bookmark
from db.database import SessionLocal


class MysqlBookmarkRepository(BookmarkRepository):
    def save(self, bookmark: BookmarkVO):
        with SessionLocal() as db:
            try:
                new_bookmark = Bookmark(
                    user_id=bookmark.user_id,
                    book_id=bookmark.book_id,
                    created_at=bookmark.created_at,
                )

                db.add(new_bookmark)
                db.commit()
            except Exception as exc:
                db.rollback()
                raise exc

    def delete(self, bookmark: BookmarkVO):
        with SessionLocal() as db:
            try:
                _bookmark = (
                    db.query(Bookmark)
                    .filter_by(user_id=bookmark.user_id, book_id=bookmark.book_id)
                    .first()
                )

                if _bookmark:
                    db.delete(_bookmark)
                    db.commit()
            except Exception as exc:
                db.rollback()
                raise exc

    def find_by_user_id_and_book_id(self, user_id, book_id) -> Optional[BookmarkVO]:
        with SessionLocal() as db:
            bookmark = (
                db.query(Bookmark)
                .filter(Bookmark.user_id == user_id, Bookmark.book_id == book_id)
                .first()
            )

            if bookmark is None:
                return None

            return BookmarkVO(
                id=bookmark.id,
                user_id=bookmark.user_id,
                book_id=bookmark.book_id,
                created_at=bookmark.created_at,
            )
