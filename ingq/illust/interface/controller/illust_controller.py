from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from dependencies.containers import Container
from illust.application.illust_service import IllustService
from illust.dto.schemas import IllustItemList, UpdateIllustRequest, UpdateIllustResponse

router = APIRouter(prefix="/v1", tags=["Illust Router"])


@router.get("/book/{book_id}/image")
@inject
def get_all_illust(
    request: Request,
    book_id: int,
    illust_service: IllustService = Depends(Provide[Container.illust_service]),
) -> IllustItemList:
    current_user = request.state.current_user
    return illust_service.get_illust_item_list_by_book_id(current_user.id, book_id)


@router.patch("/book/{book_id}/image/{illust_id}")
@inject
def update_illust(
    request: Request,
    book_id: int,
    illust_id: int,
    image_name: UpdateIllustRequest,
    illust_service: IllustService = Depends(Provide[Container.illust_service]),
) -> UpdateIllustResponse:
    current_user = request.state.current_user
    return illust_service.update_illust(current_user.id, book_id, illust_id, image_name)
