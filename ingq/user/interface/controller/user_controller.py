from fastapi import APIRouter, Depends
from user.dto.schemas import SignUpRequest, SignUpResponse

from user.application.user_service import UserService

from dependency_injector.wiring import inject, Provide
from dependencies.containers import Container

router = APIRouter(prefix="/v1")


@router.post("/signup", status_code=201)
@inject
def sign_up(
    user: SignUpRequest,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> SignUpResponse:
    _user = user_service.register_user(user)
    return _user
