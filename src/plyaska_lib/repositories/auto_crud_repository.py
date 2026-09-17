import sys
from abc import ABC, abstractmethod
from typing import Type

from src.plyaska_lib.models.data_to_objects import CreateSchemaT, ModelT, UpdateSchemaT


class AutoCRUDRepository(ABC):
    def __init__(self, model: Type[ModelT]):
        self.model = model

    def export_methods(self, module_name: str = None):
        if not module_name:
            frame = sys._getframe(1)
            module_name = frame.f_globals["__name__"]

        module = sys.modules[module_name]

        methods = {
            name: getattr(self, name)
            for name in dir(self)
            if callable(getattr(self, name))
            and not (name.startswith("__") or name.startswith("_"))
            and name != "export_methods"
        }

        for name, func in methods.items():
            setattr(module, name, func)

        return methods

    @abstractmethod
    async def create(self, item: CreateSchemaT | ModelT) -> ModelT: ...

    @abstractmethod
    async def update_or_error(self, _id, item: UpdateSchemaT | ModelT) -> ModelT: ...

    @abstractmethod
    async def update_or_create(self, _id, item: UpdateSchemaT | ModelT) -> ModelT: ...

    @abstractmethod
    async def find_all(self) -> list[ModelT]: ...

    @abstractmethod
    async def find_by_id(self, _id) -> ModelT: ...

    @abstractmethod
    async def find_by_id_or_error(self, _id) -> ModelT: ...

    @abstractmethod
    async def delete(self, _id) -> None: ...
