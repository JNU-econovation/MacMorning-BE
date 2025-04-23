from pydantic import BaseModel


class BookmarkRequest(BaseModel):
    book_id: int


class BookmarkResponse(BaseModel):
    message: str
