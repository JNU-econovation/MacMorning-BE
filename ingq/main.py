import uvicorn
from app.macmorning import create_app


app = create_app()


@app.get("/")
def hello():
    return {"Hello": "Hello FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
