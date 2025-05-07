from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from story.domain.story import Story


class StoryRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, story: Story, db: Session) -> Story:
        raise NotImplementedError

    @abstractmethod
    def find_by_book_id_and_page_number(
        self, book_id: int, page_number: int
    ) -> Optional[Story]:
        raise NotImplementedError
