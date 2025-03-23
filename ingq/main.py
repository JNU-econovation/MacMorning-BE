
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"Hello":"FastAPI"}

@app.get("/test")
def hello():
    return {"Test":"FastAPI"}

@app.get("/hi")
def hello():
    return {"Hi":"FastAPI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)