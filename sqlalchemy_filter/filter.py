from typing import Dict, List, Union

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Query

import sqlalchemy_filter.fields


__all__ = ["Filter"]


class Meta(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        meta = attrs.get("Meta")
        if not hasattr(meta, "model"):
            raise Exception("Meta model is not defined")

        cls = super().__new__(mcs, name, bases, attrs)
        fields = []
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, sqlalchemy_filter.fields.Field):
                if obj.lookup_type not in getattr(cls, "_lookup_method_map", {}):
                    raise Exception("Not registered lookup type")
                fields.append(field_name)

        cls._declared_fields = fields
        cls.model = meta.model
        return cls

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == "Filter":
            raise TypeError("Abstract class Filter cannot be instantiated")
        return super().__call__(*args, **kwargs)


class Filter(metaclass=Meta):
    _declared_fields = None
    _lookup_method_map = {
        "==": "__eq__",
        "<": "__lt__",
        ">": "__gt__",
        "<=": "__le__",
        ">=": "__ge__",
        "!=": "__ne__",
        "in": "in_",
        "not_in": "notin_",
        "like": "like",
        "ilike": "ilike",
        "notlike": "notlike",
        "notilike": "notilike",
    }

    class Meta:
        model = None

    def get_relation_model_by_name(self, name: str):
        relationships = inspect(self.model).relationships
        relationships_map = {
            relationship.mapper.class_.__name__: relationship.mapper.class_
            for relationship in relationships
        }
        return relationships_map.get(name)

    def filter_query(
        self, query: Query, filter_params: Dict[str, Union[List[str], str, bool]]
    ) -> Query:
        for param, value in filter_params.items():
            if not hasattr(self, param):
                continue

            if param not in self._declared_fields:
                continue

            field = getattr(self, param)
            field.load_value(value)

            field_relation_model = self.get_relation_model_by_name(field.relation_model)
            model = field_relation_model or self.model
            column = getattr(model, field.field_name)
            method = self._lookup_method_map[field.lookup_type]

            filter_expression = getattr(column, method)(field.get_value())
            query = query.filter(filter_expression)
        return query
