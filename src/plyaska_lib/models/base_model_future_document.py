from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import Field, model_validator

from src.plyaska_lib.models.base_model import BaseModel


class DateArchive(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BaseModelFutureDocument(DateArchive):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")

    @model_validator(mode="before")
    def normalize_id(cls, values):
        if isinstance(values, dict):
            if "id" in values and "_id" not in values:
                values["_id"] = values["id"]
        return values
