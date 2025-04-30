import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Response

from sqlalchemy.orm import Session

from ai.ai_generater import AiGenerater
from db.database import get_db
from db.models import Content
import base64

app = FastAPI()
ai = AiGenerater()
@app.get("/v1/story")
def story(db:Session = Depends(get_db)):
    try:
        content = db.query(Content).first()
        if content:
            background = "중세판타지 시대"
            history = content.content
            choice = "친구와 밤새 게임을 한다."
            result = ai.generate_story(background, history, choice)
            return {"test":"DB 연결 성공", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"DB 연결 실패: {str(e)}")

@app.get("/v1/image")
def image(db:Session = Depends(get_db)):
    try:
        content = db.query(Content).first()
        if content:
            content = content.content
            result = ai.generate_image(content)
            return {"test":"DB 연결 성공", "result":result}
        else:
            raise HTTPException(status_code=404,detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"DB 연결 실패: {str(e)}")
        

@app.get("/v1/view-image", response_class=Response)
def view_image(db: Session = Depends(get_db)):
    try:
        content = db.query(Content).first()
        if content:
            content = content.content
            result = ai.generate_image(content)
            
            if result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
                
            # base64 데이터를 바이너리로 디코딩
            image_data = base64.b64decode(result["image_data"])
            
            # 이미지 직접 반환
            return Response(
                content=image_data, 
                media_type="image/png"
            )
        else:
            raise HTTPException(status_code=404, detail="데이터가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 생성 실패: {str(e)}")
 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
