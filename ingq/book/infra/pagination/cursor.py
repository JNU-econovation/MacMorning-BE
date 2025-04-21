import base64
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from book.exception.book_exception import (
    UnsupportedStrategyException,
)
from book.infra.pagination.order_strategy import OrderStrategy


class Cursor(ABC):
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
        return cls.from_dict(cursor_data)

    @classmethod
    @abstractmethod
    def from_dict(cls, cursor_data: dict) -> "Cursor":
        pass


@dataclass
class CreatedAtCursor(Cursor):
    created_at: datetime
    book_id: int

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
