from datetime import datetime
from typing import Union, Optional, Any


__all__ = ["Field", "BooleanField", "DateTimeField", "DateField"]


class IField:
    value = None

    @staticmethod
    def validate(value, *args, **kwargs):
        raise NotImplementedError

    def load_value(self, value):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError


class Field(IField):
    def __init__(
        self,
        lookup_type: str,
        field_name: Optional[str] = None,
        relation_model: Optional[str] = None,
        **kwargs
    ):
        self.field_name = field_name
        self.lookup_type = lookup_type
        self.relation_model = relation_model

    @staticmethod
    def validate(value, *args, **kwargs):
        return value

    def load_value(self, value: str):
        self.value = self.validate(value)
        self.value = (
            value.split(",") if self.lookup_type in ["in", "not_in",] else value
        )

    def get_value(self) -> Any:
        return self.value


class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__(lookup_type="==", **kwargs)

    @staticmethod
    def validate(value: Union[bool, str], *args, **kwargs):
        if not isinstance(value, (bool, str,)):
            raise Exception("BooleanField expects bool or str")
        return value if isinstance(value, bool) else value.lower() in ["true", "1"]

    def load_value(self, value: Union[bool, str]) -> None:
        self.value = self.validate(value)


class DateTimeField(Field):
    def __init__(self, date_format="%Y-%m-%d", **kwargs):
        super().__init__(**kwargs)
        self.date_format = date_format

    @staticmethod
    def validate(
        value: Union[str, datetime], date_format=None, *args, **kwargs
    ) -> datetime:
        if not isinstance(value, (str, datetime)):
            raise Exception(
                "DateTimeField and DateField receive only str and datetime objects"
            )

        return (
            datetime.strptime(value, date_format) if isinstance(value, str) else value
        )

    def load_value(self, value: Union[str, datetime]) -> None:
        self.value = self.validate(value, date_format=self.date_format)


DateField = DateTimeField
