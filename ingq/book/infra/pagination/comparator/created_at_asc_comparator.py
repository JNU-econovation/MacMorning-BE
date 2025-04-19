from book.domain.book import Book
from book.infra.pagination.cursor import CreatedAtCursor
from book.infra.pagination.comparator.cursor_comparator import CursorComparator


class CreatedAtAscComparator(CursorComparator):
    def extract_cursor(self, standard: Book) -> CreatedAtCursor:
        return CreatedAtCursor(created_at=standard.created_at, book_id=standard.id)

    def is_after(self, standard: Book, cursor: CreatedAtCursor) -> bool:
        # 오름차순 → created_at이 더 크거나, 같고 id가 더 클 때는 더 최신이므로 다음 페이지
        return standard.created_at > cursor.created_at or (
            standard.created_at == cursor.created_at and standard.id > cursor.book_id
        )
