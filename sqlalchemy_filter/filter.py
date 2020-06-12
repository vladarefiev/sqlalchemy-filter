from typing import Callable, Dict, List, Type, Union

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Query

import sqlalchemy_filter.exceptions
import sqlalchemy_filter.fields


class Meta(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> "Callable":
        meta = attrs.get("Meta")
        if not hasattr(meta, "model"):
            raise sqlalchemy_filter.exceptions.FilterException(
                "Meta model is not defined"
            )

        cls = super().__new__(mcs, name, bases, attrs)
        cls.model = meta.model
        return cls

    def __call__(cls, *args, **kwargs) -> Type["Filter"]:
        if cls.__name__ == "Filter":
            raise sqlalchemy_filter.exceptions.FilterException(
                "Abstract class Filter cannot be instantiated"
            )
        return super().__call__(*args, **kwargs)


class Filter(metaclass=Meta):
    class Meta:
        model = None

    def get_relation_model_by_name(self, name: str) -> Dict[str, Callable]:
        relationships = inspect(self.model).relationships
        relationships_map = {
            relationship.mapper.class_.__name__: relationship.mapper.class_
            for relationship in relationships
        }
        return relationships_map.get(name)

    def get_model(self, field_relation_model: str):
        return self.get_relation_model_by_name(field_relation_model) or self.model

    def filter_query(
        self, query: Query, filter_params: Dict[str, Union[List[str], str, bool]]
    ) -> Query:
        for param, value in filter_params.items():
            if not hasattr(self, param):
                continue

            field = getattr(self, param)
            field.value = value
            model = self.get_model(field.relation_model)
            if param == "order":
                order_expression = field.get_expression()(model)
                query = query.order_by(*order_expression)
            else:
                column = getattr(model, field.field_name or param)
                filter_expression = field.get_expression()(column)
                query = query.filter(filter_expression)
        return query
