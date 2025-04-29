from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import Session

from choice.domain.choice import Choice


class ChoiceRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, choice: Choice, db: Session) -> Choice:
        raise NotImplementedError
