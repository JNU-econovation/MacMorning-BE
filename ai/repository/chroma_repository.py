from typing import List
import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from .base_vector_repository import BaseVectorRepository
from core.vector_config import vector_config
import uuid
import logging

logger = logging.getLogger(__name__)


class ChromaRepository(BaseVectorRepository):
    
    def __init__(self):
        self.config = vector_config
        
        # ChromaDB 클라이언트 초기화
        self.client = chromadb.PersistentClient(
            path=self.config.chroma_persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # OpenAI 임베딩 초기화
        self.embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model_name,
            openai_api_key=self.config.openai_api_key
        )
    
    def _get_collection_name(self, book_id: str) -> str:
        return f"{self.config.chroma_collection_name}_book_{book_id}"
    
    def _get_or_create_collection(self, book_id: str):
        collection_name = self._get_collection_name(book_id)
        try:
            collection = self.client.get_collection(name=collection_name)
            return collection
        except ValueError:
            # 컬렉션이 없으면 새로 생성
            try:
                collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"book_id": book_id}
                )
                return collection
            except Exception as e:
                logger.error(f"컬렉션 생성 실패: {str(e)}")
                raise
    
    def add_documents(self, documents: List[Document], book_id: str) -> None:
        if not documents:
            return
        
        try:
            collection = self._get_or_create_collection(book_id)
            
            # 문서 텍스트와 메타데이터 준비
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # 임베딩 생성
            embeddings = self.embeddings.embed_documents(texts)
            
            # ChromaDB에 추가
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            logger.error(f"문서 추가 중 오류 발생: {str(e)}")
            raise

    def exists_collection(self, book_id: str) -> bool:
        collection_name = self._get_collection_name(book_id)
        try:
            self.client.get_collection(name=collection_name)
            return True
        except ValueError:
            return False

    def add_single_document(self, document: Document, book_id: str) -> None:
        if not document or not document.page_content:
            logger.warning("문서가 비어있어서 저장하지 않습니다.")
            return
        
        try:
            logger.debug(f"ChromaDB에 문서 추가 시작 - book_id: {book_id}")
            collection = self._get_or_create_collection(book_id)
            logger.debug(f"컬렉션 준비 완료: {collection.name}")
            
            # 문서 텍스트와 메타데이터 준비
            text = document.page_content
            metadata = document.metadata or {}
            doc_id = str(uuid.uuid4())
            
            logger.debug(f"임베딩 생성 중... (텍스트 길이: {len(text)})")
            # 임베딩 생성
            embedding = self.embeddings.embed_query(text)
            logger.debug(f"임베딩 생성 완료 (차원: {len(embedding)})")
            
            # ChromaDB에 추가
            collection.add(
                embeddings=[embedding],
                documents=[text],  
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.info(f"ChromaDB 저장 완료 - doc_id: {doc_id}")
            
        except Exception as e:
            logger.error(f"단일 문서 추가 중 오류: {str(e)}", exc_info=True)
            raise
    
    def get_all_documents(self, book_id: str) -> List[Document]:
        if not self.exists_collection(book_id):
            return []
            
        try:
            collection = self._get_or_create_collection(book_id)
            
            # 모든 문서 조회
            results = collection.get()
            
            # Document 객체로 변환
            documents = []
            if results['documents']:
                for i, doc_text in enumerate(results['documents']):
                    metadata = results['metadatas'][i] if results['metadatas'] and i < len(results['metadatas']) else {}
                    documents.append(Document(page_content=doc_text, metadata=metadata))
            
            return documents
        except Exception as e:
            logger.error(f"모든 문서 조회 중 오류: {str(e)}")
            return []
    
    def similarity_search(self, query: str, book_id: str, k: int = 5) -> List[Document]:
        if not self.exists_collection(book_id):
            return []  # 컬렉션이 없으면 빈 리스트 반환
            
        try:
            collection = self._get_or_create_collection(book_id)
            
            # 쿼리 임베딩 생성
            query_embedding = self.embeddings.embed_query(query)
            
            # 검색 실행
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # Document 객체로 변환
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc_text in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    documents.append(Document(page_content=doc_text, metadata=metadata))
            
            return documents
        except Exception as e:
            logger.error(f"유삳 검색 중 오류: {str(e)}")
            return []
    
    def get_document_count(self, book_id: str) -> int:
        if not self.exists_collection(book_id):
            return 0
        
        collection = self._get_or_create_collection(book_id)
        return collection.count()
    
    def delete_collection(self, book_id: str) -> None:
        collection_name = self._get_collection_name(book_id)
        logger.info(f"삭제 시도할 컬렉션 이름: {collection_name}")
        try:
            # 삭제 전 확인
            if self.exists_collection(book_id):
                logger.info("컬렉션 존재함. 삭제 시작...")
                self.client.delete_collection(name=collection_name)
                logger.info("컬렉션 삭제 명령 완료")
                
                # 삭제 후 확인
                if not self.exists_collection(book_id):
                    logger.info("컬렉션 삭제 성공 확인됨")
                else:
                    logger.warning("컬렉션이 여전히 존재함")
            else:
                logger.info("삭제할 컬렉션이 존재하지 않음")
        except Exception as e:
            logger.error(f"컬렉션 삭제 중 오류: {str(e)}", exc_info=True)
            raise