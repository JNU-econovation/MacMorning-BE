from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from choice.domain.choice import Choice


class ChoiceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, choice: Choice, db: Session) -> Choice:
        raise NotImplementedError

    @abstractmethod
    def find_by_story_id(self, story_id: int, db: Session) -> Optional[Choice]:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_book_id(self, book_id: int) -> list[Choice]:
        raise NotImplementedError
