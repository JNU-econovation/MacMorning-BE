from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.application.auth_service import AuthService
from core.response.api_response_wrapper import ApiResponseWrapper
from core.response.success_response import success_response
from core.setting.load_env import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from dependencies.containers import Container
from user.application.user_service import UserService
from user.dto.schemas import SignUpRequest, SignUpResponse

router = APIRouter(prefix="/v1", tags=["Auth Router"])


ACCESS_TOKEN_EXPIRE_SECONDS = ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_TOKEN_EXPIRE_SECONDS = REFRESH_TOKEN_EXPIRE_MINUTES * 60


@router.post("/login")
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    auth_token = await auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    response_body = {"token_expires_in": f"{auth_token.token_expires_in}s"}

    response = ApiResponseWrapper(content=success_response(response_body))

    response.headers["Authorization"] = f"Bearer {auth_token.access_token}"

    response.set_cookie(
        key="refresh_token",
        value=auth_token.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_SECONDS,
        path="/",
    )

    return response


@router.post("/signup", status_code=201)
@inject
def sign_up(
    user: SignUpRequest,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> SignUpResponse:
    _user = user_service.register_user(user)
    return _user
