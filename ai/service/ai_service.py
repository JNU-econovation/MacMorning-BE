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
import logging
import re
import sys

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# 특정 로거의 레벨 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

        #이야기 첫 생성 프롬프트 템플릿 초기화
        self.start_story_prompt = PromptTemplate(
            input_variables=["genre", "character", "background", "title"],
            template="""
            제목: {title}
            이야기의 배경: {background}
            주인공 및 이야기 설정 : {character}
            장르 : {genre}

            
            제목, 이야기의 배경, 주인공 및 이야기 설정, 장르에 맞는 동화책의 이야기를 시작해주세요. 10문장이 지나면 선택지를 만들어 주세요.
            이때 마지막 문장과 선택지가 이야기처럼 자연스럽게 이어질 수 있도록 해 주세요.
            
            응답 형식:
            [이야기]
            (여기에 10문장 정도의 이야기를 작성)
            
            [선택지]
            1. (첫 번째 선택지)
            2. (두 번째 선택지)

            """
        )
        self.start_story_chain = self.start_story_prompt | self.llm | StrOutputParser()

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
            
            응답 형식:
            [이야기]
            (여기에 10문장 정도의 이야기를 작성)
            
            [선택지]
            1. (첫 번째 선택지)
            2. (두 번째 선택지)
            """
        )
        self.story_chain = self.story_prompt | self.llm | StrOutputParser()
        
        #이야기 생성 프롬프트 템플릿 초기화
        self.ending_prompt = PromptTemplate(
            input_variables=["genre", "character", "story", "background"],
            template="""
            이야기의 배경: {background}
            주인공 및 이야기 설정 : {character}
            장르 : {genre}
            지금까지의 이야기: {story}
            
            지금까지의 이야기를 바탕으로 이야기의 끝을 맺어주세요. 이야기는 10~15문장정도로 끝낼 수 있도록 해 주세요.
            """
        )
        self.ending_chain = self.ending_prompt | self.llm | StrOutputParser()

        #시놉시스 생성 프롬프트 템플릿 초기화
        self.synopsys_prompt = PromptTemplate(
            input_variables=["genre", "character"],
            template="""
            주인공 및 이야기 설정 : {character}
            장르 : {genre}
            
            주어진 배경, 주인공 및 이야기 세부설정으로 해당 장르의 간단한 동화 시놉시스와, 그에 적합한 동화 제목을 만들어줘.
            다음 JSON 형식으로만 답변해주세요:
            {{
                "title": "동화 제목",
                "synopsys": "시놉시스 내용"
            }}
            """
        )
        self.synopsys_chain = self.synopsys_prompt | self.llm | StrOutputParser()
    
    def _parse_story_and_choices(self, ai_response):
        try:
            # [이야기]와 [선택지] 섹션으로 분리
            story_match = re.search(r'\[이야기\](.*?)\[선택지\]', ai_response, re.DOTALL)
            choices_match = re.search(r'\[선택지\](.*)', ai_response, re.DOTALL)
            
            if story_match and choices_match:
                story = story_match.group(1).strip()
                choices_text = choices_match.group(1).strip()
                
                # 선택지 파싱
                choice_lines = choices_text.split('\n')
                choice1 = ""
                choice2 = ""
                
                for line in choice_lines:
                    line = line.strip()
                    if line.startswith('1.'):
                        choice1 = line[2:].strip()
                    elif line.startswith('2.'):
                        choice2 = line[2:].strip()
                
                return story, choice1, choice2
            else:
                return ai_response, "", ""
                
        except Exception as e:
            logger.error(f"이야기 파싱 중 오류: {str(e)}")
            return ai_response, "", ""

    def generate_story(self, book_id="", title="", genre="", character="", background="", choice="", is_ending=False, is_start=False):

        try:
            # 🔥 1단계: 모든 읽기 작업을 먼저 완료
            logger.info(f"📖 1단계: 기존 스토리 조회 시작 - book_id: {book_id}")
            all_vectors = self.vector_service.get_all_story_vectors(str(book_id))
            has_existing_story = len(all_vectors) > 0
            logger.info(f"📖 기존 스토리 개수: {len(all_vectors)}")
            
            relevant_context = ""
            
            # 🔥 2단계: 컨텍스트 준비 (읽기 작업)
            if is_ending and has_existing_story:
                logger.info("📖 2단계: 엔딩 컨텍스트 조회 시작")
                relevant_context = self.vector_service.get_story_context_for_ending(str(book_id))
                logger.info(f"📖 엔딩 모드 - 컨텍스트 길이: {len(relevant_context)}")
            elif choice and has_existing_story:
                logger.info(f"📖 2단계: 유사도 검색 시작 - choice: {choice[:50]}...")
                similar_docs = self.vector_service.search_similar_content(choice, str(book_id))
                logger.info(f"📖 유사 문서 개수: {len(similar_docs)}")
                
                if similar_docs:
                    # chunk_id로 정렬
                    sorted_docs = sorted(
                        similar_docs,
                        key=lambda x: x.metadata.get('chunk_id', 0)
                    )
                    relevant_context = '\n\n'.join([doc.page_content for doc in sorted_docs])
                    logger.debug(f"📖 유사한 문서 컨텍스트 길이: {len(relevant_context)}")
            
            # 🔥 3단계: AI 스토리 생성 (모든 읽기 작업 완료 후)
            logger.info("🤖 3단계: AI 스토리 생성 시작")
            
            logger.info(relevant_context)
            if is_ending:
                ai_response = self.ending_chain.invoke({

                    "genre": genre,
                    "character": character,
                    "background": background, 
                    "story": relevant_context,
                })
                logger.info("🤖 엔딩 스토리 생성 완료")
                
                # 🔥 4단계: 엔딩일 때는 삭제 (쓰기 작업)
                # logger.info("🗑️ 4단계: 스토리 삭제 시작")
                # self.vector_service.delete_story(str(book_id))
                # logger.info("🗑️ 스토리 삭제 완료")
                
                return {
                    "story": ai_response,
                }
                
            elif is_start:
                logger.info("🤖 시작 스토리 생성 중")
                ai_response = self.start_story_chain.invoke({

                    "genre": genre,
                    "character": character,
                    "background": background,
                    "title": title,
                    "choice": "이야기를 시작해주세요"
                })
            else:
                logger.info("🤖 일반 스토리 생성 중")
                ai_response = self.story_chain.invoke({
                    "genre": genre,
                    "character": character,
                    "background": background, 
                    "story": relevant_context,
                    "choice": choice
                })
            
            logger.info(f"🤖 스토리 생성 완료 - 길이: {len(ai_response)}")
            
            # 🔥 4단계: 스토리 파싱 (CPU 작업)
            logger.info("✂️ 4단계: 스토리 파싱 시작")
            story, choice1, choice2 = self._parse_story_and_choices(ai_response)
            logger.info(f"✂️ 파싱 완료 - 스토리: {len(story)}자, 선택지1: {choice1[:30] if choice1 else 'None'}...")
            
            # 🔥 5단계: 벡터 저장 (쓰기 작업 - 가장 마지막에 실행)
            logger.info("💾 5단계: 벡터 저장 시작")
            save_result = self.vector_service.add_new_content_to_vector(story, str(book_id))
            logger.info(f"💾 벡터 저장 결과: {'성공' if save_result else '실패'}")
            
            logger.info("✅ 전체 스토리 생성 과정 완료")
            return {
                "story": story,
                "choice1": choice1,
                "choice2": choice2
            }
            
        except Exception as e:
            logger.error(f"❌ 이야기 생성 중 오류가 발생했습니다: {str(e)}", exc_info=True)
            return {
                "story": None,
                "error": str(e)
            }
        
    def generate_synopsys(self, genre, character):
        try:
            character_str = f"""
            이야기 진행시점(1인칭/3인칭): {character.grammatical_person}
            시대적 배경: {character.historical_background}
            주인공 이름: {character.name}
            주인공 나이: {character.age}
            주인공 성별: {character.gender}
            주인공 설명: {', '.join(character.characteristic)}
            """

            genre_str = ', '.join(genre)

            result = self.synopsys_chain.invoke({
                "genre" : genre_str,
                "character": character_str})

            # 결과를 파싱해서 제목과 시놉시스 분리
            lines = result.split('\n')
            title = ""
            synopsys = ""
            
            current_section = ""
            for line in lines:
                if "제목:" in line or "**제목:**" in line:
                    current_section = "title"
                    title = line.replace("제목:", "").replace("**제목:**", "").strip()
                elif "시놉시스:" in line or "**시놉시스:**" in line:
                    current_section = "synopsys"
                elif line.strip() and current_section == "synopsys":
                    synopsys += line.strip() + " "

            return {
                "synopsys": synopsys.strip(),
                "title": title.strip()
            }
        except Exception as e:
            logger.error(f"시놉시스 생성 중 오류가 발생했습니다: {str(e)}")
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
                    presigned_url, content_type, s3_filename = get_presigned_url(
                        filename=filename, 
                        book_id=book_id,
                        authorization=authorization
                    )
                    
                    # S3에 이미지 업로드
                    logger.info(f"S3에 이미지 업로드 중: {presigned_url}")
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
                        "s3_filename": s3_filename,
                        "status": "uploaded_to_s3"
                    }
                except Exception as e:
                    logger.error(f"Presigned URL 처리 중 오류 발생: {str(e)}")
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
            logger.error(f"이미지 생성 중 오류가 발생했습니다: {str(e)}")
            return {
                "error": str(e),
                "image_data": None,
            }