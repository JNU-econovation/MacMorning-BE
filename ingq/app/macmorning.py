from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.cors_config import CorsConfig

from auth.interface.controller.auth_controller import router as auth_router
from user.interface.controller.user_controller import router as user_router

from dependencies.containers import Container
from db.redis_cache import redis_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_cache.close()


def create_app() -> FastAPI:
    container = Container()
    container.init_resources()
    container.wire(
        modules=[
            "user.interface.controller.user_controller",
            "auth.interface.controller.auth_controller",
        ]
    )
    app = FastAPI(lifespan=lifespan)

    app.container = container

    CorsConfig(app=app)

    app.include_router(auth_router)
    app.include_router(user_router)

    return app
