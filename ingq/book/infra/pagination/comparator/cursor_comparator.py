from abc import ABC, abstractmethod
from typing import Any


class CursorComparator(ABC):
    @abstractmethod
    def extract_cursor(self, standard: Any) -> Any:
        """객체에서 커서 정보를 추출"""
        pass

    @abstractmethod
    def is_after(self, standard: Any, cursor: Any) -> bool:
        """객체가 커서 이후에 있는 데이터인지 확인"""
        pass
