
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from core.cors_config import CorsConfig
from db.database import get_db, Base, engine
from db.models import User

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(lifespan=lifespan)

cors = CorsConfig(app=app)

@app.get("/")
def hello():
    return {"Hello":"Hello FastAPI"}

@app.get("/test")
def hello():
    return {"Test":"Test FastAPI"}

@app.get("/test-db")
def test_db_connection(db:Session = Depends(get_db)):
    try:
        user = db.query(User).first()
        if user:
            return {"test":"DB 연결 성공", "테스트 사용자":user.name}
        else:
            raise HTTPException(status_code=404,detail="사용자가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"DB 연결 실패: {str(e)}")
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)