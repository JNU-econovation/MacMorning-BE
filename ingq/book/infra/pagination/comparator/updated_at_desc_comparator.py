from book.domain.book import Book
from book.infra.pagination.comparator.cursor_comparator import CursorComparator
from book.infra.pagination.cursor import UpdatedAtCursor


class UpdatedAtDescComparator(CursorComparator):
    def extract_cursor(self, standard: Book) -> UpdatedAtCursor:
        return UpdatedAtCursor(updated_at=standard.updated_at, book_id=standard.id)

    def is_after(self, standard: Book, cursor: UpdatedAtCursor) -> bool:
        # 내림차순 → updated_at이 더 작거나, 같고 id가 더 작아야 다음 페이지
        return standard.updated_at < cursor.updated_at or (
            standard.updated_at == cursor.updated_at and standard.id < cursor.book_id
        )
