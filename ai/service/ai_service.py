from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from client.s3_client import get_presigned_url  
import os
import base64
import requests 
load_dotenv()

class AiService:
    def __init__(self, model_name="gpt-4o-mini", embedding_model_name="text-embedding-3-small", temperature=0.7):
        self.base_url = os.getenv("BE_BASE_URL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise HTTPException(status_code=500, detail="OPEN API키를 찾을 수 없습니다.")
            
        # 모델 초기화
        self.llm = ChatOpenAI(
            model_name=model_name, 
            temperature=temperature, 
            openai_api_key=self.openai_api_key)
            
        self.embedding_model = OpenAIEmbeddings(
            model=embedding_model_name,
            openai_api_key=self.openai_api_key
        )

        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100,
            chunk_overlap=30,
            encoding_name='cl100k_base'
        )
        
        # 프롬프트 템플릿 초기화
        self.story_prompt = PromptTemplate(
            input_variables=["genre", "character", "story", "background", "choice"],
            template="""
            이야기의 배경: {background}
            주인공 및 이야기 설정 : {character}
            장르 : {genre}
            지금까지의 이야기: {story}
            내 선택 : {choice}
            
            지금까지의 이야기를 바탕으로 내 선택 다음에 일어날 이야기를 만들어주세요. 10문장이 지나면 선택지를 만들어 주세요.
            이때 마지막 문장과 선택지가 이야기처럼 자연스럽게 이어질 수 있도록 해 주세요.
            """
        )
        
        self.story_chain = self.story_prompt | self.llm | StrOutputParser()

        #벡터 스토어 캐시
        self.vectorstore = None
        self.last_story = ""

    def generate_story(self, genre="", character="", background="", story="", choice=""):
        # story (이전 줄거리) 분할
        #RecursiveCharacterTextSplitter는 문서를 텍스트 조각으로 분할하는 인스턴스를 생성
        #test_splitter.split_document()는 로드된 문서 객체를 여러 개의 청크로 분할
        #100개씩 쪼개되, 30개씩 겹쳐도됨.
        try:
            if story != self.last_story :
                chunks = self.text_splitter.split_text(story)
                split_docs = [
                    Document(page_content=chunk, metadata={"chunk_id": i})
                    for i, chunk in enumerate(chunks)
                ]


                #FAISS 벡터스토어를 사용하여 문서의 임베딩을 저장
                #DistanceStrategy.COSINE은 유사도 측정기준을 코사인으로 함.
                self.vectorstore = FAISS.from_documents(
                    split_docs,
                    embedding=self.embedding_model,
                    distance_strategy=DistanceStrategy.COSINE
                )

                self.last_story = story

            #가장 유사도가 높은 문장 k개를 추출
            #lamda_mult는 유사도와 다양성 사이에 적용될 수준. 0에 가까울수록 다양성 우선, 1에 가까울수록 유사도 우선.
            if self.vectorstore is None:
                raise HTTPException(status_code=500, detail="Vectorstore가 초기화되지 않았습니다.")
            retriever = self.vectorstore.as_retriever(
                search_type='mmr',
                search_kwargs={'k': 5, 'lambda_mult': 0.15}
            )

            #검색 쿼리 - 실제로 이야기의 다음 내용을 이어가는게 아닌, 이야기의 다음 내용을 풀어나가기 위해 필요한 내용을 찾아서 반환하는 과정입니다. story_prompt랑 다름!
            query = f"내 선택 : {choice}"

            relevant_docs = retriever.get_relevant_documents(query)
            sorted_docs = sorted(relevant_docs, key=lambda x: x.metadata.get('chunk_id', 0))
            relevant_story = '\n\n'.join([doc.page_content for doc in sorted_docs])

            # 이야기 생성
            new_story = self.story_chain.invoke({
                "genre" : genre,
                "character": character,
                "background": background, 
                "story": relevant_story, 
                "choice": choice})

            return {
                "new_story": new_story,
            }
        except Exception as e:
            print(f"이야기 생성 중 오류가 발생했습니다: {str(e)}")
            return {
                "story": None,
                "error": str(e)
            }

    def generate_image(self, book_id, page, authorization, story=""):
        try:
            # OpenAI API를 사용해 이미지 생성
            result = self.openai_client.images.generate(
                model="gpt-image-1",
                size="1024x1024",
                quality="low",
                prompt=story,
            )
            # base64 형식의 이미지 데이터 추출
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            #파일명은 책 아이디 - 페이지
            filename = f"image-{book_id}-{page}.png"
            
            # 임시로 로컬에 저장
            with open(filename, "wb") as f:
                f.write(image_bytes)
            
            # Presigned URL 요청
            if book_id and authorization:
                try:
                    # BE 서버에서 Presigned URL 가져오기
                    presigned_url, content_type = get_presigned_url(
                        filename=filename, 
                        book_id=book_id,
                        base_url=self.base_url,
                        authorization=authorization
                    )
                    
                    # S3에 이미지 업로드
                    print(f"S3에 이미지 업로드 중: {presigned_url}")
                    response = requests.put(
                        presigned_url,
                        data=image_bytes,
                        headers={"Content-Type": content_type}
                    )
                    response.raise_for_status()
                    
                    # 로컬 임시 파일 삭제
                    os.remove(filename)
                    
                    return {
                        "content_type": content_type,
                        "presigned_url": presigned_url,
                        "status": "uploaded_to_s3"
                    }
                except Exception as e:
                    print(f"Presigned URL 처리 중 오류 발생: {str(e)}")
                    if os.path.exists(filename) :
                        os.remove(filename)
                    return {
                        "content_type": "image/png",
                        "local_path": filename,
                        "error": str(e),
                        "status": "error_fallback_to_local"
                    }
            else:
                return {
                    "content_type": "image/png",
                    "local_path": filename
                }
                
        except Exception as e:
            print(f"이미지 생성 중 오류가 발생했습니다: {str(e)}")
            return {
                "error": str(e),
                "image_data": None,
            }