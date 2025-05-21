from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.application.jwt_token_provider import JwtTokenProvider
from auth.utils.user_extractor import get_optional_current_user
from db.database import get_db
from dependencies.containers import Container
from story.application.story_service import StoryService
from story.dto.schemas import (
    CreateStoryWithIllustAndChoiceRequest,
    CreateStoryWithIllustAndChoiceResponse,
    GetStoryWithIllustAndChoiceResponse,
)

router = APIRouter(prefix="/v1", tags=["Story Router"])


@router.post("/book/{book_id}/story", status_code=201)
@inject
def create_story(
    request: Request,
    book_id: int,
    create_story_with_illust_and_choice_request: CreateStoryWithIllustAndChoiceRequest,
    story_service: StoryService = Depends(Provide[Container.story_service]),
    session: Session = Depends(get_db),
) -> CreateStoryWithIllustAndChoiceResponse:
    current_user = request.state.current_user
    return story_service.create_story_with_illust_and_choice(
        current_user.id, book_id, create_story_with_illust_and_choice_request, session
    )


@router.get("/book/{book_id}/story/{page_number}", status_code=200)
@inject
def get_story_with_illust_and_choice(
    request: Request,
    book_id: int,
    page_number: int,
    story_service: StoryService = Depends(Provide[Container.story_service]),
    jwt_token_provider: JwtTokenProvider = Depends(
        Provide[Container.jwt_token_provider]
    ),
    session: Session = Depends(get_db),
) -> GetStoryWithIllustAndChoiceResponse:
    current_user = get_optional_current_user(request, jwt_token_provider)
    user_id = current_user.id if current_user else None
    return story_service.get_story_with_illust_and_choice(
        user_id, book_id, page_number, session
    )
