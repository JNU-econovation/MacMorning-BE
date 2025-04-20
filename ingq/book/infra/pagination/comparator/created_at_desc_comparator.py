from book.domain.book import Book
from book.infra.pagination.comparator.cursor_comparator import CursorComparator
from book.infra.pagination.cursor import CreatedAtCursor


class CreatedAtDescComparator(CursorComparator):
    def extract_cursor(self, standard: Book) -> CreatedAtCursor:
        return CreatedAtCursor(created_at=standard.created_at, book_id=standard.id)

    def is_after(self, standard: Book, cursor: CreatedAtCursor) -> bool:
        # 내림차순 → created_at이 더 작거나, 같고 id가 더 작아야 다음 페이지
        return standard.created_at < cursor.created_at or (
            standard.created_at == cursor.created_at and standard.id < cursor.book_id
        )
