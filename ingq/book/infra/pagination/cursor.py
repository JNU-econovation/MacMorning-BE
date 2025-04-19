from dataclasses import dataclass
from datetime import datetime

from typing import Optional, Union, Any

from book.infra.pagination.order_strategy import OrderStrategy
from book.exception.book_exception import (
    OrderStrategyAndCursorParameterMismatchException,
    UnsupportedStrategyException,
)


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


def parse_cursor(cursor: str) -> dict:
    cursor_parts = cursor.split(",")
    cursor_dict = {
        k: v for k, v in (part.split(":", 1) for part in cursor_parts if ":" in part)
    }
    return cursor_dict


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

    cursor_dict = parse_cursor(cursor)

    if order_strategy in [
        OrderStrategy.CREATED_AT_DESC,
        OrderStrategy.CREATED_AT_ASC,
    ]:
        if "created_at" not in cursor_dict or "book_id" not in cursor_dict:
            raise OrderStrategyAndCursorParameterMismatchException(
                "CreatedAt을 정렬 전략으로 선택하셨습니다. 커서 값으로 created_at과 book_id가 있는지 확인해주세요."
            )
        try:
            created_at = datetime.fromisoformat(cursor_dict["created_at"])
            book_id = int(cursor_dict["book_id"])
            return CreatedAtCursor(created_at=created_at, book_id=book_id)
        except (ValueError, TypeError) as err:
            raise OrderStrategyAndCursorParameterMismatchException(
                "ISO 형식의 시간이 맞는지, book_id가 int인지 확인해주세요."
            ) from err

    elif order_strategy in [
        OrderStrategy.UPDATED_AT_DESC,
        OrderStrategy.UPDATED_AT_ASC,
    ]:
        if "updated_at" not in cursor_dict or "book_id" not in cursor_dict:
            raise OrderStrategyAndCursorParameterMismatchException(
                "UpdatedAt을 정렬 전략으로 선택하셨습니다. 커서 값으로 updated_at과 book_id가 있는지 확인해주세요."
            )
        try:
            updated_at = datetime.fromisoformat(cursor_dict["updated_at"])
            book_id = int(cursor_dict["book_id"])
            return UpdatedAtCursor(updated_at=updated_at, book_id=book_id)
        except (ValueError, TypeError) as err:
            raise OrderStrategyAndCursorParameterMismatchException(
                "ISO 형식의 시간이 맞는지, book_id가 int인지 확인해주세요."
            ) from err

    # TODO: 추후 구현 예정
    elif order_strategy in [
        OrderStrategy.BOOKMARK_COUNT_DESC,
        OrderStrategy.BOOKMARK_COUNT_ASC,
    ]:
        raise NotImplementedError(
            f"정렬 전략 {order_strategy}에 대한 커서 처리가 아직 구현되지 않았습니다."
        )

    elif order_strategy in [
        OrderStrategy.VIEW_COUNT_DESC,
        OrderStrategy.VIEW_COUNT_ASC,
    ]:
        raise NotImplementedError(
            f"정렬 전략 {order_strategy}에 대한 커서 처리가 아직 구현되지 않았습니다."
        )

    else:
        raise UnsupportedStrategyException(
            f"{order_strategy}는 지원하지 않는 order_strategy입니다."
        )
