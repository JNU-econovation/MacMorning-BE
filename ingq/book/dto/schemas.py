from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Book 생성 관련 DTO
class Character(BaseModel):
    name: Optional[str] = Field(
        default=None, max_length=10, description="주인공 이름 (최대 10자)"
    )

    age: Optional[int] = Field(default=None, ge=0, description="주인공 나이 (0 이상)")

    gender: Optional[Literal["남성", "여성"]] = Field(
        default=None, description="주인공 성별 ('남성' 또는 '여성')"
    )

    characteristic: Optional[list[str]] = Field(
        default_factory=list, description="주인공 특징"
    )


class CharacterRequest(Character):
    pass


class CharacterResponse(Character):
    pass


class CreateBookRequest(BaseModel):
    genre: list[str] = Field(
        ..., min_items=1, max_items=3, description="최대 3개까지 장르를 선정해주세요."
    )
    gamemode: bool = Field(
        ...,
        description="게임 모드 여부 (True: 게임 모드 활성화, False: 게임 모드 비활성화)",
    )
    character: CharacterRequest = Field(description="주인공 정보")
    title: str = Field(
        ..., min_length=1, max_length=30, description="책 제목(최소 1글자, 최대 30글자)"
    )
    background: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="주제 및 줄거리(최소 1글자, 최대 100글자)",
    )
    is_in_progress: bool = Field(
        True, description="이야기 진행 여부 (True: 진행중, False: 완성)"
    )

    @field_validator("genre")
    @classmethod
    def validate_unique_genres(cls, genres: list[str]) -> list[str]:
        if len(genres) != len(set(genres)):
            raise ValueError("장르는 중복이 불가능합니다.")
        return genres


# 논의 후 변경 예정
class CreateBookResponse(BaseModel):
    id: int
    user_id: str
    genre: list[str]
    gamemode: bool
    character: CharacterResponse
    title: str
    background: str
    is_in_progress: bool
    created_at: datetime
    updated_at: datetime


# ============================================================================
# Book 조회 관련 DTO
class BookItem(BaseModel):
    """
    'Home', '내 책', '이야기 도서관' 페이지에서 반환 할 Book Response DTO

    Home: Best 동화책, 내가 쓴 동화책, 내가 찜한 동화책 4개씩 반환할 때 사용
    내 책: 전체, 진행중인 이야기, 완성된 이야기 반환에 사용
    이야기 도서관: Best 동화책, 모든 동화책, 내가 찜한 동화책 반환에 사용
    """

    id: int
    title_img_url: str
    title: str
    author: str
    background: Optional[str] = None
    is_bookmarked: Optional[bool] = Field(
        default=None,
        description="로그인 완료된 사용자에게만 제공, 비로그인 시 미포함 필드",
    )


# ============================================================================
# 커서 기반 페이지 네이션 관련 DTO
class PageInfo(BaseModel):
    has_next: bool
    total_count: int


class PaginatedBookItem(BaseModel):
    books: list[BookItem]
    next_cursor: Optional[Any]
    page_info: PageInfo
