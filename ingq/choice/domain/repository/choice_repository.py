from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import Session

from choice.domain.choice import Choice


class ChoiceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, choice: Choice, db: Session) -> Choice:
        raise NotImplementedError

    @abstractmethod
    def find_by_story_id(self, story_id: int, db: Session) -> Choice:
        raise NotImplementedError
