import logging
from enum import Enum
from http import HTTPMethod
from typing import Type

import inflection
from beanie import PydanticObjectId
from fastapi import APIRouter
from fastapi.routing import APIRoute

from src.plyaska_lib.temp.exceptions.errors.http import NotFoundedHTTPException
from src.plyaska_lib.temp.exceptions.errors.repository import NotFoundedError
from src.plyaska_lib.db.cache import redis_cache
from src.plyaska_lib.models.create_update_dto_maker import (
    make_create_schema,
    make_update_schema,
)
from src.plyaska_lib.models.data_to_objects import CreateSchemaT, ModelT, UpdateSchemaT
from src.plyaska_lib.repositories.auto_crud_repository import AutoCRUDRepository
from src.plyaska_lib.repositories.beanie_auto_crud_repository import BeanieAutoCRUDRepository


class CRUDRouter:
    """
    Example::

        from pydantic import BaseModel

        class UserModel(BaseModel):
            name: str

        class UserCreate(BaseModel):
            name: str

        router = CRUDRouter[UserModel, UserCreate, UserCreate](
            model=UserModel,
            create_schema=UserCreate,
            update_schema=UserCreate
            ).router
    """

    def __init__(
        self,
        model: Type[ModelT],
        create_schema: Type[CreateSchemaT] | None = None,
        update_schema: Type[UpdateSchemaT] | None = None,
        prefix: str | None = None,
        tags: list[str | Enum] | None = None,
        exclude: list[str] | None = None,
        find_all_cached: bool = True,
    ):
        if exclude is None:
            exclude = []
        self.model = model
        self.create_schema = create_schema or make_create_schema(model)
        self.update_schema = update_schema or make_update_schema(model)
        self.prefix = (
            prefix or f"/{inflection.underscore(model.__name__).replace('_', '-')}s"
        )
        self.router = APIRouter(prefix=self.prefix, tags=tags or [model.__name__])
        self.repository: AutoCRUDRepository = BeanieAutoCRUDRepository(self.model)

        # change type "item" parameter
        self.create = self._create(self.create_schema)
        self.update = self._update(self.update_schema)
        if find_all_cached:
            # self.find_all = redis_cache(self.find_all, cache_who=self.model, cache_by='all')
            self.find_all = redis_cache(cache_who=self.model, cache_by="all")(
                self.find_all
            )

        routes_define = {
            self.create.__name__: lambda: self.router.post(
                "/", response_model=model, status_code=201
            )(self.create),
            self.find_all.__name__: lambda: self.router.get(
                "/", response_model=list[model]
            )(self.find_all),
            self.find_by_id.__name__: lambda: self.router.get(
                "/{id}", response_model=model
            )(self.find_by_id),
            self.update.__name__: lambda: self.router.patch(
                "/{id}", response_model=model
            )(self.update),
            self.delete.__name__: lambda: self.router.delete("/{id}")(self.delete),
        }

        routes_could_define = {
            key: value for key, value in routes_define.items() if key not in exclude
        }

        for define in routes_could_define.values():
            define()

    def delete_query(
        self,
        path: str,
        router: APIRouter | None = None,
        method: HTTPMethod | None = None,
        name: str | None = None,
    ):
        """

        :param name:
        :param method:
        :param router:
        :param path: Template: prefix/{path}/
        :return:
        :Example:
        Example::

            router = crud_router.delete_query('items', router, name=get_items_v1.__name__)
        """
        if router is None:
            router = self.router
        if len(path) > 0:
            if path[0] == "/":
                path = path[1:]
        logging.debug(f"Routes was: {router.routes}")
        router.routes = [
            r
            for r in router.routes
            if not (
                isinstance(r, APIRoute)
                and r.path == f"{self.prefix}/{path}"
                and (method is None or r.methods == [method.value])
                and (name is None or r.name == name)
            )
        ]
        logging.getLogger(__name__)
        logging.debug(f"Routes now: {router.routes}")
        if router is None:
            self.router = router
        return router

    def _create(self, schema_type: CreateSchemaT | ModelT):
        async def create(item: schema_type):
            return await self.repository.create(item)

        return create

    def _update(self, schema_type: UpdateSchemaT | ModelT):
        async def update(id: PydanticObjectId, item: schema_type):
            try:
                return await self.repository.update_or_error(id, item)
            except NotFoundedError:
                raise NotFoundedHTTPException()

        return update

    async def find_all(self):
        return await self.repository.find_all()

    @redis_cache("{.model}:{id}")
    async def find_by_id(self, id: PydanticObjectId):
        try:
            return await self.repository.find_by_id_or_error(id)
        except NotFoundedError:
            raise NotFoundedHTTPException()

    async def delete(self, id: PydanticObjectId):
        try:
            await self.repository.delete(id)
            return {"is_deleted": True}
        except NotFoundedError:
            raise NotFoundedHTTPException()
