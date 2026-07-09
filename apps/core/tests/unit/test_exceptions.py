import pytest
from apps.core.domain.exceptions import (
    DomainError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    PermissionDeniedError,
    ConflictError,
    RateLimitError,
    ExternalServiceError,
)


class TestDomainExceptions:

    def test_domain_error_defaults(self):
        exc = DomainError()
        assert exc.status_code == 400
        assert exc.code == "domain_error"

    def test_domain_error_custom_message(self):
        exc = DomainError(message="Что-то пошло не так")
        assert exc.message == "Что-то пошло не так"

    def test_not_found_error(self):
        exc = NotFoundError()
        assert exc.status_code == 404
        assert exc.code == "not_found"

    def test_validation_error_with_details(self):
        exc = ValidationError(field="email")
        assert exc.details == {"field": "email"}

    def test_authentication_error(self):
        exc = AuthenticationError()
        assert exc.status_code == 401

    def test_permission_denied_error(self):
        exc = PermissionDeniedError()
        assert exc.status_code == 403

    def test_conflict_error(self):
        exc = ConflictError()
        assert exc.status_code == 409

    def test_rate_limit_error(self):
        exc = RateLimitError()
        assert exc.status_code == 429

    def test_external_service_error(self):
        exc = ExternalServiceError()
        assert exc.status_code == 502