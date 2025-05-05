from pydantic import BaseModel


class UploadImageRequest(BaseModel):
    filename: str


class UploadImageResponse(BaseModel):
    presigned_url: str
    filename: str
    content_type: str
