from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from django.db.models import Model

T = TypeVar('T', bound=Model)
DTO = TypeVar('DTO')

class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, obj_id: Any) -> T:
        ...

    @abstractmethod
    def save(self, obj: T) -> T:
        ...

    @abstractmethod
    def delete(self, obj: T) -> T:
        ...

class AbstractService(ABC, Generic[DTO]):

    @abstractmethod
    def execute(self, dto: DTO) -> Any:
        ...
