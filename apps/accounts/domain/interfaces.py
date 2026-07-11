from abc import abstractmethod
from apps.accounts.models import User
from apps.core.domain.interfaces import AbstractRepository

class UserRepositoryInterface(AbstractRepository[User]):
    @abstractmethod
    def get_by_username(self, username: str) -> User:
        ...

    @abstractmethod
    def create_user(self, **fields) -> User:
        ...