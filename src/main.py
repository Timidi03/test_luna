from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import router
from src.core.exception_handlers import (
    exception_handler,
    internal_error_handler,
    not_found_handler,
    validation_handler,
)
from src.core.exceptions import (
    NotFoundError,
    ServiceError,
    ValidationError,
)
from src.core.middleware import APIKeyMiddleware
from src.event_funcs import lifespan


def create_app():
    app = FastAPI(title="Organization API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        allow_methods=["*"],
    )

    app.add_middleware(APIKeyMiddleware)

    app.include_router(router)

    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(ServiceError, internal_error_handler)
    app.add_exception_handler(ValidationError, validation_handler)
    app.add_exception_handler(Exception, exception_handler)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Organization API",
            version="1.0.0",
            description="API with static API key auth",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
            }
        }

        openapi_schema["security"] = [{"ApiKeyAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:create_app", host="0.0.0.0", port=8000)
