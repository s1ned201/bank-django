from typing import Any


class DomainError(Exception):
    """Базовое исключение"""
    default_message: str = "Произошла ошибка в бизнес-логике"
    default_code: str = "domain_error"
    default_status_code: int = 400

    def __init__(self, message: str | None = None, code: str | None = None, **kwargs: Any) -> None:
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.status_code = self.default_status_code
        self.details = kwargs
        super().__init__(self.message)

class NotFoundError(DomainError):
    """Ресурс не найден"""
    default_message = "Ресурс не найден"
    default_code = "not_found"
    default_status_code = 404

class ValidationError(DomainError):
    """Ошибка валидации данных"""
    default_message = "Ошибка валидации данных"
    default_code = "validation_error"
    default_status_code = 422


class AuthenticationError(DomainError):
    """Ошибка аутентификации"""
    default_message = "Ошибка аутентификации"
    default_code = "authentication_error"
    default_status_code = 401


class PermissionDeniedError(DomainError):
    """Доступ запрещён"""
    default_message = "Доступ запрещён"
    default_code = "permission_denied"
    default_status_code = 403


class ConflictError(DomainError):
    """Конфликт данных"""
    default_message = "Конфликт данных"
    default_code = "conflict"
    default_status_code = 409


class RateLimitError(DomainError):
    """Превышен лимит запросов"""
    default_message = "Слишком много запросов. Попробуйте позже."
    default_code = "rate_limit_exceeded"
    default_status_code = 429


class ExternalServiceError(DomainError):
    """Ошибка внешнего сервиса"""
    default_message = "Внешний сервис недоступен"
    default_code = "external_service_error"
    default_status_code = 502