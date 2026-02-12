from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.config import config


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/docs", "/openapi.json", "/redoc"]

        if request.url.path in excluded_paths:
            return await call_next(request)

        client_key = request.headers.get("X-API-Key")

        if not client_key or client_key != config.API_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"},
            )

        return await call_next(request)
