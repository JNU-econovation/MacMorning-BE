import base64
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from book.exception.book_exception import (
    InvalidCursorException,
    UnsupportedStrategyException,
)
from book.infra.db_models.book import Book
from book.infra.pagination.order_strategy import OrderStrategy


class Cursor(ABC):
    expected_fields: set[str] = set()

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def encode(cls, cursor: "Cursor") -> str:
        cursor_data = cursor.to_dict()
        cursor_json = json.dumps(cursor_data)
        return base64.urlsafe_b64encode(cursor_json.encode("utf-8")).decode("utf-8")

    @classmethod
    def decode(cls, encoded_cursor: str) -> "Cursor":
        decoded_json = base64.urlsafe_b64decode(encoded_cursor).decode("utf-8")
        cursor_data = json.loads(decoded_json)
        cls.validate_fields(cursor_data)
        return cls.from_dict(cursor_data)

    @classmethod
    def validate_fields(cls, cursor_data: dict):
        unexpected_fields = set(cursor_data.keys()) - cls.expected_fields
        if unexpected_fields:
            raise InvalidCursorException(
                f"{cls.__name__}에 유효하지 않은 필드가 포함되어 있습니다: {unexpected_fields}, 정렬 전략과 커서값이 일치한지 확인해주세요."
            )

    @classmethod
    @abstractmethod
    def from_dict(cls, cursor_data: dict) -> "Cursor":
        pass


@dataclass
class CreatedAtCursor(Cursor):
    created_at: datetime
    book_id: int

    expected_fields = {"created_at", "book_id"}

    def to_dict(self) -> dict:
        return {"created_at": self.created_at.isoformat(), "book_id": self.book_id}

    @classmethod
    def from_dict(cls, cursor_data: dict) -> "CreatedAtCursor":
        created_at = datetime.fromisoformat(cursor_data["created_at"])
        book_id = cursor_data["book_id"]
        return CreatedAtCursor(created_at, book_id)


@dataclass
class UpdatedAtCursor(Cursor):
    updated_at: datetime
    book_id: int

    expected_fields = {"updated_at", "book_id"}

    def to_dict(self) -> dict:
        return {"updated_at": self.updated_at.isoformat(), "book_id": self.book_id}

    @classmethod
    def from_dict(cls, cursor_data: dict) -> "UpdatedAtCursor":
        updated_at = datetime.fromisoformat(cursor_data["updated_at"])
        book_id = cursor_data["book_id"]
        return UpdatedAtCursor(updated_at=updated_at, book_id=book_id)


@dataclass
class BookmarkCountCursor(Cursor):
    bookmark_count: int
    book_id: int

    expected_fields = {"bookmark_count", "book_id"}

    def to_dict(self) -> dict:
        return {"bookmark_count": self.bookmark_count, "book_id": self.book_id}

    @classmethod
    def from_dict(cls, cursor_data: dict) -> "BookmarkCountCursor":
        bookmark_count = cursor_data["bookmark_count"]
        book_id = cursor_data["book_id"]
        return BookmarkCountCursor(bookmark_count=bookmark_count, book_id=book_id)


def validate_and_get_cursor(
    cursor: str, order_strategy: OrderStrategy
) -> Optional[Union[CreatedAtCursor, UpdatedAtCursor, BookmarkCountCursor]]:
    """
    커서 형식 및 타입 검증 후 Cursor 객체 반환
    """
    if not cursor:
        return None

    if (
        order_strategy == OrderStrategy.CREATED_AT_DESC
        or order_strategy == OrderStrategy.CREATED_AT_ASC
    ):
        return CreatedAtCursor.decode(cursor)
    elif (
        order_strategy == OrderStrategy.UPDATED_AT_DESC
        or order_strategy == OrderStrategy.UPDATED_AT_ASC
    ):
        return UpdatedAtCursor.decode(cursor)
    elif (
        order_strategy == OrderStrategy.BOOKMARK_COUNT_DESC
        or order_strategy == OrderStrategy.BOOKMARK_COUNT_ASC
    ):
        return BookmarkCountCursor.decode(cursor)
    else:
        raise UnsupportedStrategyException(
            f"{order_strategy}는 지원하지 않는 order_strategy입니다."
        )


def create_next_cursor(
    books: list[Book],
    order_strategy: OrderStrategy,
    has_next: bool,
) -> Optional[str]:
    if not has_next or not books:
        return None

    last_book = books[-1]

    cursor_config = {
        OrderStrategy.CREATED_AT_ASC: (CreatedAtCursor, "created_at"),
        OrderStrategy.CREATED_AT_DESC: (CreatedAtCursor, "created_at"),
        OrderStrategy.UPDATED_AT_ASC: (UpdatedAtCursor, "updated_at"),
        OrderStrategy.UPDATED_AT_DESC: (UpdatedAtCursor, "updated_at"),
        OrderStrategy.BOOKMARK_COUNT_ASC: (BookmarkCountCursor, "bookmark_count"),
        OrderStrategy.BOOKMARK_COUNT_DESC: (BookmarkCountCursor, "bookmark_count"),
    }

    cursor_class, field_name = cursor_config[order_strategy]
    field_value = getattr(last_book, field_name)
    cursor_params = {field_name: field_value, "book_id": last_book.id}
    cursor_instance = cursor_class(**cursor_params)

    return Cursor.encode(cursor_instance)
