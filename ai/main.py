import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from ai.story_ai import generate_story
from db.database import get_db
from db.models import Content

app = FastAPI()

@app.get("/")
def test(db:Session = Depends(get_db)):
    try:
        content = db.query(Content).first()
        if content:
            background = "중세판타지 시대"
            history = content.content
            choice = "친구와 밤새 게임을 한다."
            result = generate_story(background, history, choice)
            return {"test":"DB 연결 성공", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"DB 연결 실패: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
