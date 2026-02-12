from typing import Any


class AppError(Exception):
    def __init__(self, message: str, data: Any = None):
        super().__init__(message)
        self.message = message
        self.data = data

    def __str__(self):
        return self.message


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass


class ServiceError(AppError):
    pass
