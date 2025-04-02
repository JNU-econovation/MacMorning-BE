from fastapi.middleware.cors import CORSMiddleware


class CorsConfig:
    def __init__(self, app):
        origins = ["http://localhost:3000", "https://localhost:3000"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
