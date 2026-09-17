from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Generic

from httpx import Response

from plyaska_lib.controllers.crud_router import ModelT


@dataclass
class ResponseModel(Generic[ModelT]):
    response: Response
    model: ModelT


@dataclass
class ResponseDo(Generic[ModelT], ResponseModel[ModelT]):
    do: Callable[[], Coroutine[Any, Any, ResponseModel[ModelT]]]
