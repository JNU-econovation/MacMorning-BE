from typing import List, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from repository.base_vector_repository import BaseVectorRepository
from repository.chroma_repository import ChromaRepository
from core.vector_config import vector_config
import logging

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self, repository: Optional[BaseVectorRepository] = None):
        self.config = vector_config
        self.repository = repository or ChromaRepository()
        
        # 텍스트 분할기 초기화
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            encoding_name=self.config.encoding_name
        )
    
    #모든 벡터 조회
    def get_all_story_vectors(self, book_id: str) -> List[Document]:
        try:
            return self.repository.get_all_documents(book_id)
        except Exception as e:
            logger.error(f"모든 벡터 조회 중 오류 발생: {str(e)}")
            return []
    
    #유사도 검색
    def search_similar_content(self, choice: str, book_id: str) -> List[Document]:
        try:
            # choice를 기반으로 유사도 검색
            #chroma db는 기본적으로 코사인 유사도 방식
            similar_docs = self.repository.similarity_search(
                query=choice,
                book_id=book_id,
                k=self.config.search_k
            )
            return similar_docs
        except Exception as e:
            logger.error(f"유사도 검색 중 오류 발생: {str(e)}")
            return []

    # 벡터 저장    
    def add_new_content_to_vector(self, new_content: str, book_id: str) -> bool:
        try:
            logger.info(f"벡터 저장 시작 - book_id: {book_id}, 내용 길이: {len(new_content)}")

            # 청크 분할            
            chunks = self.text_splitter.split_text(new_content)
            logger.debug(f"생성된 청크 개수: {len(chunks)}")
            
            if not chunks:
                logger.warning("청크가 생성되지 않았습니다.")
                return False
            
            # 현재 문서 개수 조회 (chunk_id 계산용)
            current_count = 0
            try:
                current_count = self.repository.get_document_count(book_id)
                logger.debug(f"현재 문서 개수: {current_count}")
            except Exception as e:
                logger.error(f"현재 문서 개수 조회 실패: {str(e)}")
            
            # 각 청크를 개별적으로 저장
            for i, chunk in enumerate(chunks):
                logger.info(f"청크 {i+1}/{len(chunks)} 저장 중...")
                document = Document(
                    page_content=chunk,
                    metadata={
                        "chunk_id": current_count + i,
                        "book_id": book_id,
                        "source": "new_story",
                        "content_type": "generated"
                    }
                )
                self.repository.add_single_document(document, book_id)
                logger.info(f"청크 {i+1} 저장 완료")
            
            logger.info(f"모든 청크 저장 완료 - 총 {len(chunks)}개")
            return True
            
        except Exception as e:
            logger.error(f"새로운 내용 벡터 저장 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
    #최근 스토리 청크 조회
    def get_recent_story_chunks(self, book_id: str, count: int = 5) -> List[Document]:
        try:
            all_docs = self.repository.get_all_documents(book_id)
            if not all_docs:
                return []
            
            # chunk_id로 정렬하여 최근 것들 가져오기
            sorted_docs = sorted(
                all_docs,
                key=lambda x: x.metadata.get('chunk_id', 0),
                reverse=True  # 최신순
            )
            
            return sorted_docs[:count]
            
        except Exception as e:
            logger.error(f"최근 스토리 청크 조회 중 오류 발생: {str(e)}")
            return []
    

    #엔딩 스토리 컨텍스트 조회
    def get_story_context_for_ending(self, book_id: str) -> str:
        try:
            recent_chunks = self.get_recent_story_chunks(book_id, 5)
            all_chunks = self.repository.get_all_documents(book_id)
            
            if not all_chunks:
                return ""
            
            # 최근 내용 (직접적 컨텍스트)
            recent_content = '\n'.join([doc.page_content for doc in recent_chunks])
            
            # 전체 스토리의 키워드 추출 (간접적 컨텍스트)
            all_content = '\n'.join([doc.page_content for doc in all_chunks])
            
            context = f"최근 이야기:\n{recent_content}\n\n전체 스토리 키워드: {all_content[:200]}..."
            return context
            
        except Exception as e:
            logger.error(f"엔딩 컨텍스트 조회 중 오류 발생: {str(e)}")
            return ""
            
    #스토리 삭제        
    def delete_story(self, book_id: str) -> bool:
        try:
            self.repository.delete_collection(book_id)   
            return True
        except Exception as e:
            logger.error(f"스토리 삭제 중 오류 발생: {str(e)}")
            return False