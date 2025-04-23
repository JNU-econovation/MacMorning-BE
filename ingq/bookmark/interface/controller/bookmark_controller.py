from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from bookmark.application.bookmark_service import BookmarkService
from bookmark.dto.schemas import BookmarkRequest, BookmarkResponse
from dependencies.containers import Container

router = APIRouter(prefix="/v1", tags=["Bookmark Router"])


@router.post("/bookmark")
@inject
def toggle_bookmark(
    request: Request,
    bookmark_request: BookmarkRequest,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
) -> BookmarkResponse:
    current_user = request.state.current_user
    return bookmark_service.toggle_bookmark(current_user.id, bookmark_request)
