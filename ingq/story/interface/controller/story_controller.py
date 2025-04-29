from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.containers import Container
from story.application.story_service import StoryService
from story.dto.schemas import (
    CreateStoryWithIllustAndChoiceRequest,
    CreateStoryWithIllustAndChoiceResponse,
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
