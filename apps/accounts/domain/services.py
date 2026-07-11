from apps.accounts.domain.interfaces import UserRepositoryInterface
from apps.accounts.domain.dto import RegistrationDTO
from apps.accounts.models import User, TwoFACode
from apps.core.domain.exceptions import ConflictError, ValidationError
from datetime import timedelta
from django.utils import timezone
from apps.accounts.infrastructure.tasks import send_2fa_code


class RegistrationService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def execute(self, dto: RegistrationDTO) -> User:
        if self.user_repo.model_class.objects.filter(username=dto.username).exists():
            raise ConflictError("Пользователь с таким username уже существует.")
        if self.user_repo.model_class.objects.filter(email=dto.email).exists():
            raise ConflictError("Пользователь с таким email уже существует.")
        user = self.user_repo.create_user(
            username=dto.username,
            email=dto.email,
            password=dto.password,
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone_number=dto.phone_number,
        )
        return user

class TwoFAService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def send_code(self, user):
        if not user.telegram_id or not user.is_telegram_verified:
            raise ValidationError("Telegram не привязан или не подтверждён.")

        TwoFACode.objects.filter(user=user, is_used=False).update(is_used=True)
        code = TwoFACode.generate_code()
        expires_at = timezone.now() + timedelta(minutes=5)

        TwoFACode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at,
        )

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[2FA] Код {code} для пользователя {user.username} (Telegram ID: {user.telegram_id})")

        return code
        # send_2fa_code.delay(user.id, user.telegram_id, code)
        # return code

    def verify_code(self, user, code, ip_address=None):
        try:
            twofa_code = TwoFACode.objects.get(
                user=user,
                code=code,
                is_used=False
            )
        except TwoFACode.DoesNotExist:
            raise ValidationError("Неверный код или код уже использован.")

        if twofa_code.is_expired():
            raise ValidationError("Срок действия кода истёк.")

        twofa_code.is_used = True
        if ip_address:
            twofa_code.ip_address = ip_address
        twofa_code.save()
        return True