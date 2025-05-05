from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.interface.controller.auth_controller import router as auth_router
from book.interface.controller.book_controller import router as book_router
from bookmark.interface.controller.bookmark_controller import router as bookmark_router
from config.cors_config import CorsConfig
from config.openapi_config import custom_openapi
from core.auth_middleware import AuthMiddleware
from core.exception.error_handler import register_exception_handlers
from core.response.api_response_wrapper import ApiResponseWrapper
from db.redis_cache import redis_cache
from dependencies.containers import Container
from story.interface.controller.story_controller import router as story_router
from upload_image.interface.controller.upload_controller import router as upload_router


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
            "book.interface.controller.book_controller",
            "bookmark.interface.controller.bookmark_controller",
            "story.interface.controller.story_controller",
            "upload_image.interface.controller.upload_controller",
        ]
    )
    app = FastAPI(lifespan=lifespan, default_response_class=ApiResponseWrapper)

    exempt_paths = [
        "/v1/token/reissue",
        "/v1/login",
        "/v1/signup",
        "/v1/books",
        "/v1/books/best",
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
    app.include_router(book_router)
    app.include_router(bookmark_router)
    app.include_router(story_router)
    app.include_router(upload_router)

    app.openapi = lambda: custom_openapi(app, exempt_paths)

    register_exception_handlers(app)

    return app
