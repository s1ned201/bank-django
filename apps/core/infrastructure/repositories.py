from typing import Any, Type, TypeVar
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist
from apps.core.domain.interfaces import AbstractRepository
from apps.core.domain.exceptions import NotFoundError

T = TypeVar("T", bound=Model)

class BaseRepository(AbstractRepository[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_by_id(self, obj_id: Any) -> T:
        try:
            return self.model_class.objects.get(pk=obj_id)
        except ObjectDoesNotExist:
            raise NotFoundError(
                message=f"{self.model_class.__name__} с id={obj_id} не найден."
            )

    def save(self, obj: T) -> T:
        obj.save()
        return obj

    def delete(self, obj: T) -> None:
        obj.delete()