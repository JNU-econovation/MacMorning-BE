from fastapi import FastAPI, HTTPException, Header
from service.ai_service import AiService
from client.book_client import get_story, get_book
from pydantic import BaseModel

app = FastAPI()
ai = AiService()
hardcoded_book_info = {
    1: {
        "genre": "판타지",  
        "character": "용감한 기사 아서. 마법검을 소유하고 있으며, 정의감이 강하다.",
        "background": "중세 시대의 마법이 존재하는 왕국. 어둠의 마법사가 왕국을 위협하고 있다."
    },
    2: {
        "genre": "SF",
        "character": "우주 탐험가 제나. 뛰어난 과학자이며 호기심이 많다.",
        "background": "2150년 미래, 인류가 여러 행성에 식민지를 건설한 시대. 외계 생명체와의 첫 접촉이 이루어지려 하고 있다."
    }
}

class StoryRequest(BaseModel):
    choice: str


@app.post("/v1/book/{book_id}")
def synopsys(book_id: int, authorization: str = Header(None)):
    try:
        book_info = get_book(book_id, authorization)
        if book_info :
            genre = book_info.get("genre")
            character = book_info.get("character")
            background = book_info.get("background")
            result = ai.generate_synopsys(genre, character, background)
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

@app.post("/v1/book/{book_id}/story")
def story(book_id: int, request: StoryRequest, authorization: str = Header(...)):
    try:
        # book_info = get_book(book_id, authorization)
        book_info = hardcoded_book_info.get(book_id)

        if book_info:
            genre = book_info.get("genre")
            character = book_info.get("character")
            background = book_info.get("background")
            result = ai.generate_story(
                genre = genre,
                character = character,
                background = background,
                choice = request.choice,
                book_id = book_id)
            return {"status": "success", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"책 조회 실패: {e}") from e


@app.post("/v1/book/{book_id}/story/end")
def end_story(book_id: int, authorization: str=Header(None)):
    try:
        # book_info = get_book(book_id, authorization)
        book_info = hardcoded_book_info.get(book_id)

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
            return {"status": "success", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"책 조회 실패: {e}") from e
    
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
