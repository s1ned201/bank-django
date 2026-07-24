from apps.core.domain.services import AuditService

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Логируем только аутентифицированных пользователей
        if hasattr(request, 'user') and request.user.is_authenticated:
            AuditService.log(
                user=request.user,
                action=f"{request.method} {request.path}",
                ip_address=request.META.get('REMOTE_ADDR'),
            )
        return response