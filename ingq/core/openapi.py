from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI, exempt_paths):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Macmorning API",
        version="1.0.0",
        description="API 문서입니다.",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path, methods in openapi_schema["paths"].items():
        if path not in exempt_paths:
            for method in methods.values():
                method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema
