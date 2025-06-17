from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class CreateChoiceRequest(BaseModel):
    first_choice: str = Field(..., description="1번 선택지(LLM 생성)")
    second_choice: str = Field(..., description="2번 선택지(LLM 생성)")
    third_choice: Optional[str] = Field(
        default=None, description="3번 선택지(선택사항: 사용자 직접 입력)"
    )
    my_choice: Literal[1, 2, 3] = Field(
        ..., description="사용자의 선택(게임 모드 시 실패 여부와 상관 X)"
    )
    is_success: bool = Field(
        default=True,
        description="기본 모드: 항상 True, 게임 모드: 게임에 승리한 경우 True, 실패한 경우 False",
    )


class CreateChoiceResponse(BaseModel):
    choice_id: int
    story_id: int
    first_choice: str
    second_choice: str
    third_choice: Optional[str]
    my_choice: int
    is_success: bool
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Choice 조회 관련 DTO
class ChoiceItem(BaseModel):
    choice_id: int
    story_id: int
    first_choice: str
    second_choice: str
    third_choice: Optional[str]
    my_choice: int
    is_success: bool
    created_at: datetime
    updated_at: datetime


# ============================================================================
class LastChoiceItem(BaseModel):
    choice_id: int
    story_id: int
    choice_content: str  # 1, 2, 3 번 선택지 중 사용자가 입력한 선택지
    my_choice: int
    is_success: bool
    reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class LastChoiceItemList(BaseModel):
    choices: list[LastChoiceItem]
