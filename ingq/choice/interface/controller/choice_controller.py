from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from auth.application.jwt_token_provider import JwtTokenProvider
from auth.utils.user_extractor import get_optional_current_user
from choice.application.choice_service import ChoiceService
from choice.dto.schemas import LastChoiceItem, LastChoiceItemList, UpdateReasonRequest
from dependencies.containers import Container

router = APIRouter(prefix="/v1", tags=["Choice Router"])


@router.get("/book/{book_id}/choice")
@inject
def get_all_selected_choice(
    request: Request,
    book_id: int,
    choice_service: ChoiceService = Depends(Provide[Container.choice_service]),
    jwt_token_provider: JwtTokenProvider = Depends(
        Provide[Container.jwt_token_provider]
    ),
) -> LastChoiceItemList:
    current_user = get_optional_current_user(request, jwt_token_provider)
    user_id = current_user.id if current_user else None
    return choice_service.get_selected_choice_item_by_book_id(user_id, book_id)


@router.post("/book/{book_id}/choice/{choice_id}")
@inject
def update_choice(
    request: Request,
    book_id: int,
    choice_id: int,
    reason: UpdateReasonRequest,
    choice_service: ChoiceService = Depends(Provide[Container.choice_service]),
) -> LastChoiceItem:
    current_user = request.state.current_user
    return choice_service.update_selected_choice(
        current_user.id, book_id, choice_id, reason
    )
