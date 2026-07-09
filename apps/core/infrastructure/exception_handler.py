from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from apps.core.domain.exceptions import DomainError

def custom_exception_handler(exc, context):
    """
       Кастомный обработчик исключений для DRF.
       Перехватывает DomainError и возвращает унифицированный JSON.
       Для остальных исключений используется стандартное поведение DRF.
    """
    if isinstance(exc, DomainError):
        response_data = {
            'error': {
                'code': exc.code,
                'message': str(exc),
            }
        }
        if exc.details:
            response_data['error']['details'] = exc.details
        return Response(
            response_data,
            status=exc.status_code
        )

    response = exception_handler(exc, context)
    return response