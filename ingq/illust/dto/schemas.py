from datetime import datetime

from pydantic import BaseModel, Field


class CreateIllustRequest(BaseModel):
    image_url: str = Field(..., description="이미지 주소")


class CreateIllustResponse(BaseModel):
    illust_id: int
    story_id: int
    image_url: str
    created_at: datetime
    updated_at: datetime
