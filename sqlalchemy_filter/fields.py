import abc
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

import sqlalchemy_filter.exceptions

__all__ = ["Field", "BooleanField", "DateTimeField", "DateField", "JsonField"]


class IField(metaclass=abc.ABCMeta):
    _value = None
    _lookup_method_map = None
    relation_model = None

    @staticmethod
    @abc.abstractmethod
    def validate(value, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_expression(self):
        raise NotImplementedError


class Field(IField):
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

    def __init__(
        self,
        lookup_type: str,
        field_name: Optional[str] = None,
        relation_model: Optional[str] = None,
        **kwargs
    ):
        if lookup_type not in self._lookup_method_map:
            raise sqlalchemy_filter.exceptions.LookTypeException(
                "Not registered lookup type"
            )

        self.field_name = field_name
        self.lookup_type = lookup_type
        self.relation_model = relation_model

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = self.validate(value)
        if self.lookup_type in ["in", "not_in"] and isinstance(value, str):
            value: List[str] = [v.strip() for v in value.split(",")]

        self._value = value

    @staticmethod
    def validate(value, *args, **kwargs):
        return value

    def get_expression(self):
        method = self._lookup_method_map[self.lookup_type]

        def expression(column):
            return getattr(column, method)(self._value)

        return expression


class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__(lookup_type="==", **kwargs)

    @staticmethod
    def validate(value: Union[bool, str], *args, **kwargs):
        if not isinstance(value, (bool, str,)):
            raise sqlalchemy_filter.exceptions.FieldException(
                "BooleanField expects bool or str"
            )
        return value if isinstance(value, bool) else value.lower() in ["true", "1"]

    @Field.value.setter
    def value(self, value: Union[bool, str]) -> None:
        self._value = self.validate(value)


class DateTimeField(Field):
    _lookup_method_map = {
        "==": "__eq__",
        "<": "__lt__",
        ">": "__gt__",
        "<=": "__le__",
        ">=": "__ge__",
        "!=": "__ne__",
    }

    def __init__(self, date_format="%Y-%m-%d", **kwargs):
        super().__init__(**kwargs)
        self.date_format = date_format

    @staticmethod
    def validate(
        value: Union[str, datetime], date_format=None, *args, **kwargs
    ) -> datetime:
        if not isinstance(value, (str, datetime, date)):
            raise sqlalchemy_filter.exceptions.FieldException(
                "DateTimeField and DateField receive only str and datetime objects"
            )

        return (
            datetime.strptime(value, date_format) if isinstance(value, str) else value
        )

    @Field.value.setter
    def value(self, value: Union[str, datetime]) -> None:
        self._value = self.validate(value, date_format=self.date_format)


class JsonField(Field):
    _lookup_method_map = {
        "#>>": "op",
        "->>": "op",
    }

    def __init__(
        self,
        lookup_type: str = None,
        lookup_path: Optional[str] = None,
        not_equal=False,
        *args,
        **kwargs
    ):
        super().__init__(lookup_type, *args, **kwargs)
        self.lookup_path = lookup_path
        self.not_equal = not_equal

    def get_expression(self):
        method = self._lookup_method_map[self.lookup_type]

        def expression(column):
            filter_statement = getattr(column, method)(self.lookup_type)(
                self.lookup_path
            )
            compare_method = "__ne__" if self.not_equal else "__eq__"
            return getattr(filter_statement, compare_method)(self._value)

        return expression


class OrderField(IField):
    @property
    def value(self) -> Dict[str, str]:
        return self._value

    @staticmethod
    def validate(value: str, *args, **kwargs) -> List[str]:
        if not isinstance(value, str):
            raise sqlalchemy_filter.exceptions.FieldException(
                "OrderField expects str value"
            )
        return [i.strip() for i in value.split(",")]

    @value.setter
    def value(self, value: str):
        value = self.validate(value)
        result = {}
        for field in value:
            order = "asc"
            if field.startswith("-"):
                field = field[1:]
                order = "desc"
            result[field] = order

        self._value = result

    def get_expression(self):
        def expression(model):
            order_columns = []
            for field, order in self.value.items():
                column = getattr(model, field)
                order_columns.append(getattr(column, order)())
            return order_columns

        return expression


DateField = DateTimeField
