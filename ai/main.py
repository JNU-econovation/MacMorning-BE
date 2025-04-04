import uvicorn
from ai.story_ai import generate_story
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test():
    return generate_story()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
