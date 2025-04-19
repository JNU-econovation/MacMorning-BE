from dataclasses import dataclass
from datetime import datetime

from typing import Optional, Union, Any

from book.infra.pagination.order_strategy import OrderStrategy


@dataclass
class CreatedAtCursor:
    created_at: datetime
    book_id: int


@dataclass
class UpdatedAtCursor:
    updated_at: datetime
    book_id: int


@dataclass
class BookmarkCountCursor:
    bookmark_count: int
    book_id: int


@dataclass
class ViewCountCursor:
    view_count: int
    book_id: int


def validate_and_get_cursor(
    cursor: Any, order_strategy: OrderStrategy
) -> Optional[
    Union[CreatedAtCursor, UpdatedAtCursor, BookmarkCountCursor, ViewCountCursor]
]:
    """
    커서 형식 및 타입 검증

    Cursor 반환
    """
    if not cursor:
        return None

    try:
        cursor_parts = cursor.split(",")
        cursor_dict = {
            k: v
            for k, v in (part.split(":", 1) for part in cursor_parts if ":" in part)
        }

        if order_strategy in [
            OrderStrategy.CREATED_AT_DESC,
            OrderStrategy.CREATED_AT_ASC,
        ]:
            if "created_at" not in cursor_dict or "book_id" not in cursor_dict:
                raise ValueError("created_at 과 book_id 값을 확인해주세요.")
            try:
                created_at = datetime.fromisoformat(cursor_dict["created_at"])
                book_id = int(cursor_dict["book_id"])
                return CreatedAtCursor(created_at=created_at, book_id=book_id)
            except (ValueError, TypeError):
                return None

        elif order_strategy in [
            OrderStrategy.UPDATED_AT_DESC,
            OrderStrategy.UPDATED_AT_ASC,
        ]:
            if "updated_at" not in cursor_dict or "book_id" not in cursor_dict:
                raise ValueError("updated_at 과 book_id 값을 확인해주세요.")
            try:
                updated_at = datetime.fromisoformat(cursor_dict["updated_at"])
                book_id = int(cursor_dict["book_id"])
                return UpdatedAtCursor(updated_at=updated_at, book_id=book_id)
            except (ValueError, TypeError):
                return None

        # TODO: 추후 구현 예정
        elif order_strategy in [
            OrderStrategy.BOOKMARK_COUNT_DESC,
            OrderStrategy.BOOKMARK_COUNT_ASC,
        ]:
            return None

        elif order_strategy in [
            OrderStrategy.VIEW_COUNT_DESC,
            OrderStrategy.VIEW_COUNT_ASC,
        ]:
            return None

    except ValueError as ve:
        print(f"value Error 발생: {ve}")
        raise

    except Exception as exc:
        print(f"정렬 전략 설정 및 커서 사이에서 에러 발생: {exc}")
        raise

    return None
