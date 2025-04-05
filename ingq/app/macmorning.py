from fastapi import FastAPI

from core.cors_config import CorsConfig

from user.interface.controller.user_controller import router as user_router

from dependencies.containers import Container


def create_app() -> FastAPI:
    app = FastAPI()

    container = Container()
    container.init_resources()
    container.wire(modules=["user.interface.controller.user_controller"])
    app.container = container

    CorsConfig(app=app)

    app.include_router(user_router)

    return app
