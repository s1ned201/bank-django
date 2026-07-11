from apps.core.infrastructure.repositories import BaseRepository
from apps.accounts.domain.interfaces import UserRepositoryInterface
from apps.accounts.models import User
from apps.core.domain.exceptions import NotFoundError, ValidationError

class UserRepository(BaseRepository[User], UserRepositoryInterface):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, username: str) -> User:
        try:
            return self.model_class.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFoundError(f"Пользователь с username '{username}' не найден.")

    def create_user(self, **fields) -> User:
        if not fields.get('username') or not fields.get('password'):
            raise ValidationError("username и password обязательны.")
        user = self.model_class(**{k: v for k, v in fields.items() if k != 'password'})
        user.set_password(fields['password'])
        user.save()
        return user