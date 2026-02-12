from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    NotFoundError,
    ServiceError,
)
from src.core.logger import get_logger

logger = get_logger(__name__)


async def not_found_handler(request: Request, exc: NotFoundError):
    logger.warning(
        f"NotFoundError | Path: {request.url.path} | " f"Message: {exc.message}"
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


async def validation_handler(request: Request, exc: NotFoundError):
    logger.warning(
        f"ValidationError | Path: {request.url.path} | " f"Message: {exc.message}"
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


async def internal_error_handler(request: Request, exc: ServiceError):
    logger.exception(
        f"ServerError | Path: {request.url.path} | " f"Message: {exc.message}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


async def exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
