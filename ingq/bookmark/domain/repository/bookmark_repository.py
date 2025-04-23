from abc import ABCMeta, abstractmethod
from typing import Optional

from bookmark.domain.bookmark import Bookmark


class BookmarkRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, bookmark: Bookmark):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bookmark: Bookmark):
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id_and_book_id(
        self, user_id: str, book_id: int
    ) -> Optional[Bookmark]:
        raise NotImplementedError
