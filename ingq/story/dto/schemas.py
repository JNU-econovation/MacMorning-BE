from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from choice.dto.schemas import CreateChoiceRequest, CreateChoiceResponse
from illust.dto.schemas import CreateIllustRequest, CreateIllustResponse


# ============================================================================
# Story 생성 관련 DTO
class CreateStoryRequest(BaseModel):
    book_id: int = Field(..., description="책 ID")
    page_number: int = Field(..., description="책 페이지")
    story_text: str = Field(..., description="이야기")


class CreateStoryResponse(BaseModel):
    story_id: int
    book_id: int
    page_number: int
    story_text: str
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Story 생성 시 이미지와 선택지 생성 관련 DTO
class CreateStoryWithIllustAndChoiceRequest(BaseModel):
    story: CreateStoryRequest
    illust: Optional[CreateIllustRequest] = Field(
        default=None, description="저장된 이미지 주소"
    )
    choice: Optional[CreateChoiceRequest] = Field(
        default=None, description="선택지(마지막 페이지의 경우 생략)"
    )


class CreateStoryWithIllustAndChoiceResponse(BaseModel):
    story: CreateStoryResponse
    illust: Optional[CreateIllustResponse] = None
    choice: Optional[CreateChoiceResponse] = None
