from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import Session

from story.domain.story import Story


class StoryRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, story: Story, db: Session) -> Story:
        raise NotImplementedError
