from fastapi import FastAPI, HTTPException, Header
from service.ai_service import AiService
from client.book_client import get_story, get_book
from client.token_client import token_verification
from pydantic import BaseModel
import logging
import sys

app = FastAPI()
ai = AiService()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class StoryRequest(BaseModel):
    choice: str

class Character(BaseModel):
    grammatical_person: str
    historical_background: str
    name: str
    age: str
    gender: str
    characteristic: list[str]

class BookRequest(BaseModel):
    title: str
    background: str
    genre: list[str]
    character: Character

@app.post("/v1/book/{book_id}/story/start")
def startStory(book_id: int, request: BookRequest, authorization: str = Header(...)):
    try:
        title = request.title
        background = request.background
        genre = request.genre
        character = request.character
        result = ai.generate_story(
            title=title,
            background=background,
            genre=genre,
            character=character,
            book_id=book_id,
            is_start=True
        )
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {
            "success": False, 
            "data": None, 
            "error": {
                "code": "SV001", 
                "status": 500, 
                "message": "서버 내부 오류", 
                "error": str(e)
            }
        }

@app.post("/v1/book/{book_id}/story")
def story(book_id: int, request: StoryRequest, authorization: str = Header(...)):
    try:
        book_info = get_book(book_id, authorization)

        if book_info :
            genre = book_info.get("genre")
            character = book_info.get("character")
            background = book_info.get("background")
            result = ai.generate_story(
                genre = genre,
                character = character,
                background = background,
                choice = request.choice,
                book_id = book_id)
            return {"success": True, "data": result, "error": None}
        else:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "BOOK001",
                    "status": 404,
                    "message": "데이터가 없습니다.",
                }
            }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "DB001",
                "status": 500,
                "message": "DB 연결 실패",
                "error": str(e)
            }
        }


@app.post("/v1/book/{book_id}/story/end")
def end_story(book_id: int, authorization: str = Header(...)):
    try:
        book_info = get_book(book_id, authorization)

        if book_info:
            genre = book_info.get("genre")
            character = book_info.get("character")
            background = book_info.get("background")
            result = ai.generate_story(
                genre = genre,
                character = character,
                background = background,
                book_id = book_id,
                is_ending=True)
            return {"success": True, "data": result, "error": None}
        else:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "BOOK001",
                    "status": 404,
                    "message": "데이터가 없습니다."
                }
            }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "DB001",
                "status": 500,
                "message": "DB 연결 실패",
                "error": str(e)
            }
        }
    
@app.post("/v1/book/{book_id}/image/{page_number}")
def image(book_id: int,page_number: int, authorization: str = Header(None)):
    try:
        content = get_story(book_id, page_number, authorization)
        if content:
            result = ai.generate_image(book_id,page_number,authorization,content)
            return {"status": "success", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"DB 연결 실패: {str(e)}")
