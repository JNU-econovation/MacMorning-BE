from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import Base, engine
from core.cors_config import CorsConfig

from user.interface.controller.user_controller import router as user_router

from dependencies.containers import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )

    container = Container()
    container.init_resources()
    container.wire(modules=["user.interface.controller.user_controller"])
    app.container = container

    CorsConfig(app=app)

    app.include_router(user_router)

    return app
