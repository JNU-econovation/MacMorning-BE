from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from client.s3_client import get_presigned_url  
from service.vector_service import VectorService
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
            
        # 이야기 생성용 모델 초기화
        self.llm = ChatOpenAI(
            model_name=model_name, 
            temperature=temperature, 
            openai_api_key=self.openai_api_key)

        #이미지 생성용 모델 초기화
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        #벡터 서비스 초기화
        self.vector_service = VectorService()
        
        #이야기 생성 프롬프트 템플릿 초기화
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

        #시놉시스 생성 프롬프트 템플릿 초기화
        self.synopsys_prompt = PromptTemplate(
            input_variables=["genre", "character", "background"],
            template="""
            이야기의 배경: {background}
            주인공 및 이야기 설정 : {character}
            장르 : {genre}
            
            주어진 배경, 주인공 및 이야기 세부설정으로 해당 장르의 간단한 동화 시놉시스를 만들어줘.
            """
        )
        self.synopsys_chain = self.synopsys_prompt | self.llm | StrOutputParser()

    def generate_story(self, book_id, genre="", character="", background="", choice=""):
        try:
            all_vectors = self.vector_service.get_all_story_vectors(str(book_id))
            has_existing_story = len(all_vectors) > 0
            
            relevant_context = ""
            
            #이전 내용과 선택지가 있다 - 두번째 이야기 생성부터의 로직
            if choice and has_existing_story:
                similar_docs = self.vector_service.search_similar_content(choice, str(book_id))
                
                if similar_docs:
                    # chunk_id로 정렬
                    # 벡터화는 순서를 보장하지 않기 때문에, 이야기를 순서대로 정렬하는 과정입니다
                    sorted_docs = sorted(
                        similar_docs,
                        key=lambda x: x.metadata.get('chunk_id', 0)
                    )
                    relevant_context = '\n\n'.join([doc.page_content for doc in sorted_docs])
                    print(f"유사한 문서: {relevant_context}")
            
            new_story = self.story_chain.invoke({
                "genre": genre,
                "character": character,
                "background": background, 
                "story": relevant_context,
                "choice": choice or "이야기를 시작해주세요"
            })
            
            #새로운 내용 벡터화 하여 저장
            self.vector_service.add_new_content_to_vector(new_story, str(book_id))
            
            return {
                "new_story": new_story,
            }
        except Exception as e:
            print(f"이야기 생성 중 오류가 발생했습니다: {str(e)}")
            return {
                "story": None,
                "error": str(e)
            }
        
    def generate_synopsys(self, genre="", character="", background=""):
        try:
            synopsys = self.synopsys_chain.invoke({
                "genre" : genre,
                "character": character,
                "background": background, })

            return {
                "synopsys": synopsys,
            }
        except Exception as e:
            print(f"시놉시스 생성 중 오류가 발생했습니다: {str(e)}")
            return {
                "synopsys": None,
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