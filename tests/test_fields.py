from datetime import date, datetime

import pytest

from sqlalchemy_filter import exceptions, fields


def test_field_with_unknown_lookup_type():
    with pytest.raises(exceptions.LookTypeException):
        fields.Field(lookup_type="foo")


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (True, True),
        ("True", True),
        ("true", True),
        ("1", True),
        ("0", False),
        ("", False),
        ("false", False),
        ("False", False),
    ],
)
def test_boolean_field(input_data, expected):
    field = fields.BooleanField(field_name="foo")
    field.value = input_data
    assert field.value is expected


def test_boolean_field_with_bad_value():
    with pytest.raises(exceptions.FieldException):
        field = fields.BooleanField(field_name="foo")
        field.value = 1


@pytest.mark.parametrize(
    "input_data, date_format, expected, error_class",
    [
        ("2020-01-01", "%Y-%m-%d", datetime(year=2020, month=1, day=1), None),
        ("2020-10-01", "%Y-%d-%m", datetime(year=2020, month=1, day=10), None),
        ("Jun 1 2020", "%b %d %Y", datetime(year=2020, month=6, day=1), None),
        (
            datetime(year=2020, month=6, day=1),
            None,
            datetime(year=2020, month=6, day=1),
            None,
        ),
        (date(year=2020, month=6, day=1), None, date(year=2020, month=6, day=1), None,),
        ("Jun 1 2020", "%Y %d %m", datetime(year=2020, month=6, day=1), ValueError),
    ],
)
def test_date_field(input_data, date_format, expected, error_class):
    field = fields.DateField(field_name="foo", date_format=date_format, lookup_type=">")
    if error_class:
        with pytest.raises(error_class):
            field.value = input_data
    else:
        field = fields.DateField(
            field_name="foo", date_format=date_format, lookup_type=">"
        )
        field.value = input_data
        assert field.value == expected


def test_datetime_field_with_bad_value():
    with pytest.raises(exceptions.FieldException):
        field = fields.DateTimeField(field_name="foo", lookup_type="==")
        field.value = 1


@pytest.mark.parametrize(
    "input_data, date_format, expected, error_class",
    [
        (
            "2020-01-01 13:22:05",
            "%Y-%m-%d %H:%M:%S",
            datetime(year=2020, month=1, day=1, hour=13, minute=22, second=5),
            None,
        ),
        (
            datetime(year=2020, month=1, day=1, hour=13, minute=22, second=5),
            "%Y-%m-%d %H:%M:%S",
            datetime(year=2020, month=1, day=1, hour=13, minute=22, second=5),
            None,
        ),
        (
            "2020-01-01 1:22:05PM",
            "%Y-%m-%d %H:%M:%S",
            datetime(year=2020, month=1, day=1, hour=13, minute=22, second=5),
            ValueError,
        ),
        (
            "Jun 1 2020  1:33PM",
            "%b %d %Y %I:%M%p",
            datetime(year=2020, month=6, day=1, hour=13, minute=33),
            None,
        ),
        (
            datetime(year=2020, month=6, day=1, hour=13, minute=33),
            "%b %d %Y %I:%M%p",
            datetime(year=2020, month=6, day=1, hour=13, minute=33),
            None,
        ),
        (
            "Jun 1 2020  13:33PM",
            "%b %d %Y %I:%M%p",
            datetime(year=2020, month=6, day=1, hour=13, minute=33),
            ValueError,
        ),
    ],
)
def test_datetime_field(input_data, date_format, expected, error_class):
    field = fields.DateTimeField(
        field_name="foo", date_format=date_format, lookup_type=">"
    )
    if error_class:
        with pytest.raises(error_class):
            field.value = input_data
    else:
        field.value = input_data
        assert field.value == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("-foo,bar", {"foo": "desc", "bar": "asc"}),
        ("foo, bar", {"foo": "asc", "bar": "asc"}),
        ("-foo,-bar", {"foo": "desc", "bar": "desc"}),
    ],
)
def test_order_field(input_data, expected):
    field = fields.OrderField()
    field.value = input_data
    assert field.value == expected
