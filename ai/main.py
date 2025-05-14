from fastapi import FastAPI, HTTPException, Header, Body
from service.ai_service import AiService
from client.book_client import get_story, get_book, get_all_story

app = FastAPI()
ai = AiService()

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
def story(book_id: int, choice: int = Body(None), authorization: str = Header(...)):
    try:
        book_info = get_book(book_id, authorization)
        story = get_all_story(book_id, authorization)
        if book_info and story:
            genre = book_info.get("genre")
            character = book_info.get("character")
            background = book_info.get("background")
            result = ai.generate_story(genre, character, background, story, choice)
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
