from typing import Any, Generic, TypeVar

from ninja import Schema
from pydantic import Field
from pydantic.generics import GenericModel

TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class CamelSchema(Schema):
    class Config(Schema.Config):
        alias_generator = convert_field_to_camel_case
        allow_population_by_field_name = True


class PaginationOut(CamelSchema):
    offset: int
    limit: int
    total: int


class ListPaginatedResponse(CamelSchema, GenericModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOut


class ApiResponse(CamelSchema, GenericModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)
