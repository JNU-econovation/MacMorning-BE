from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseVectorRepository(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document], book_id: str) -> None:
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, book_id: str, k: int = 5) -> List[Document]:
        pass
    
    @abstractmethod
    def exists_collection(self, book_id: str) -> bool:
        pass
    
    @abstractmethod
    def add_single_document(self, document: Document, book_id: str) -> None:
        pass
    
    @abstractmethod
    def get_all_documents(self, book_id: str) -> List[Document]:
        pass
    
    @abstractmethod
    def get_document_count(self, book_id: str) -> int:
        pass

    @abstractmethod
    def delete_collection(self, book_id: str) -> None:
        pass