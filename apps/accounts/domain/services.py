import logging
import requests
from django.conf import settings
from apps.accounts.domain.interfaces import UserRepositoryInterface
from apps.accounts.domain.dto import RegistrationDTO
from apps.accounts.models import User, TwoFACode
from apps.core.domain.exceptions import ConflictError, ValidationError
from datetime import timedelta
from django.utils import timezone
from apps.telegram_bot.tasks import send_2fa_code

logger = logging.getLogger(__name__)


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

        send_2fa_code.delay(user.id, user.telegram_id, code)
        return code

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

    def send_telegram_bind_code(self, user, telegram_id):
        """Отправляет код подтверждения на указанный Telegram ID"""
        TwoFACode.objects.filter(user=user, is_used=False).update(is_used=True)
        code = TwoFACode.generate_code()
        expires_at = timezone.now() + timedelta(minutes=5)
        TwoFACode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at,
        )
        send_2fa_code.delay(user.id, telegram_id, code)
        return code

    def verify_telegram_bind_code(self, user, code, telegram_id):
        """Проверяет код и привязывает Telegram к пользователю"""
        try:
            twofa_code = TwoFACode.objects.get(user=user, code=code, is_used=False)
        except TwoFACode.DoesNotExist:
            raise ValidationError("Неверный код.")
        if twofa_code.is_expired():
            raise ValidationError("Код истёк.")
        twofa_code.is_used = True
        twofa_code.save()
        user.telegram_id = telegram_id
        user.is_telegram_verified = True
        user.save()
        # avatar
        if not user.telegram_avatar_url:
            avatar_url = self._fetch_telegram_avatar(telegram_id)
            if avatar_url:
                user.telegram_avatar_url = avatar_url
                user.save(update_fields=['telegram_avatar_url'])
        return True

    def _fetch_telegram_avatar(self, telegram_id):
        """Получает URL аватарки Telegram."""
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not token:
            return None
        try:
            url = f"https://api.telegram.org/bot{token}/getUserProfilePhotos?user_id={telegram_id}&limit=1"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if data.get('ok') and data['result']['photos']:
                photos = data['result']['photos'][0]
                file_id = photos[-1]['file_id']
                file_resp = requests.get(f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}").json()
                if file_resp.get('ok'):
                    file_path = file_resp['result']['file_path']
                    return f"https://api.telegram.org/file/bot{token}/{file_path}"
            else:
                logger.info(f"No photos found for user {telegram_id}")
        except Exception as e:
            logger.error(f"Failed to fetch Telegram avatar: {e}")
        return None