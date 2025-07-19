from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from illust.domain.illust import Illust


class IllustRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, illust: Illust, db: Session) -> Illust:
        raise NotImplementedError

    @abstractmethod
    def find_by_story_id(self, story_id: int, db: Session) -> Optional[Illust]:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_book_id(self, book_id: int) -> list[Illust]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, illust_id: int) -> Optional[Illust]:
        raise NotImplementedError

    @abstractmethod
    def update_illust(self, illust: Illust) -> Illust:
        raise NotImplementedError
