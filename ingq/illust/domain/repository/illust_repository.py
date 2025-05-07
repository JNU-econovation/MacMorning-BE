from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import Session

from illust.domain.illust import Illust


class IllustRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, illust: Illust, db: Session) -> Illust:
        raise NotImplementedError
