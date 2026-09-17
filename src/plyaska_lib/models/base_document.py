from typing import Type, TypeVar

from beanie import Delete, Document, Insert, Replace, Update, after_event

from plyaska_lib.string import camel_to_db_name

T = TypeVar("T", bound=Type[Document])


def auto_collection(cls: T):
    if not hasattr(cls, "Settings"):

        class Settings:
            name: str

        cls.Settings = Settings

    cls.Settings.name = camel_to_db_name(cls.__name__)
    return cls


class BaseDocument(Document):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        auto_collection(cls)

    def cache_key(self, id):
        return f"{self.get_settings().name}:{str(id)}"

    @after_event(Insert)
    @after_event(Replace)
    @after_event(Delete)
    @after_event(Update)
    async def clear_cache(self):
        from src.main import main

        r = await main.get_connect_cache()

        await r.delete(self.cache_key(self.id))
        await r.delete(self.cache_key("all"))
