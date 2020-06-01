from datetime import datetime
from typing import List, Union


class Field:
    value = None

    def __init__(self, field_name, lookup_type, relation_model=None, **kwargs):
        self.field_name = field_name
        self.lookup_type = lookup_type
        self.relation_model = relation_model

    @staticmethod
    def validate(value, *args, **kwargs):
        return value

    def load_value(self, value: str) -> None:
        self.validate(value)

        self.value: Union[List[str], str] = value.split(",") if self.lookup_type in [
            "in",
            "not_in",
        ] else value

    def get_value(self) -> Union[List[str], str, bool]:
        return self.value


class BooleanField(Field):
    def __init__(self, field_name: str, **kwargs):
        super().__init__(field_name, lookup_type="==", **kwargs)

    def load_value(self, value: Union[bool, str]) -> None:
        self.value = (
            value if isinstance(value, bool) else value.lower() in ["true", "1"]
        )


class DateTimeField(Field):
    def __init__(
        self,
        field_name,
        lookup_type,
        relation_model=None,
        date_format="%Y-%m-%d",
        **kwargs
    ):
        super().__init__(field_name, lookup_type, relation_model, **kwargs)
        self.date_format = date_format

    @staticmethod
    def validate(value, date_format, *args, **kwargs):
        if not isinstance(value, (str, datetime)):
            raise Exception()
        return datetime.strptime(value, date_format)

    def load_value(self, value: Union[str, datetime]) -> None:
        self.value = self.validate(value, self.date_format)


DateField = DateTimeField