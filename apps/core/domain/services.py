from apps.core.models import AuditLog

class AuditService:
    @staticmethod
    def log(user, action: str, ip_address: str = None, details: dict = None):
        AuditLog.objects.create(
            user=user,
            action=action,
            ip_address=ip_address,
            details=details or {},
        )