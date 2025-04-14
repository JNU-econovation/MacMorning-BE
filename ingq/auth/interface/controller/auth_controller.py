# login, reissue

# logout을 어떻게 할지? 공통 api 써버릴까?
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from auth.application.auth_service import AuthService

from dependency_injector.wiring import inject, Provide
from dependencies.containers import Container

from dotenv import load_dotenv
import os

router = APIRouter(prefix="/v1", tags=["Auth Router"])


load_dotenv()
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")) * 60


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

    response = JSONResponse(
        content={"token_expires_in": f"{auth_token.token_expires_in}s"}
    )

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
