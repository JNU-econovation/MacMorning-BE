from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.cors_config import CorsConfig
from core.auth_middleware import AuthMiddleware
from config.openapi_config import custom_openapi

from auth.interface.controller.auth_controller import router as auth_router

from dependencies.containers import Container
from db.redis_cache import redis_cache

from core.response.api_response_wrapper import ApiResponseWrapper
from core.exception.error_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_cache.close()


def create_app() -> FastAPI:
    container = Container()
    container.init_resources()
    container.wire(
        modules=[
            "auth.interface.controller.auth_controller",
        ]
    )
    app = FastAPI(lifespan=lifespan, default_response_class=ApiResponseWrapper)

    exempt_paths = [
        "/v1/token/reissue",
        "/v1/login",
        "/v1/signup",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]

    app.container = container
    app.add_middleware(
        AuthMiddleware, exempt_paths, jwt_token_provider=container.jwt_token_provider()
    )

    CorsConfig(app=app)

    app.include_router(auth_router)

    app.openapi = lambda: custom_openapi(app, exempt_paths)

    register_exception_handlers(app)

    return app
