import pytest

from sqlalchemy_filter import exceptions, fields, filter
from tests import models


def test_base_filter_class():
    with pytest.raises(exceptions.FilterException):
        filter.Filter()


def test_filter_class_without_meta_model():
    with pytest.raises(exceptions.FilterException):
        type(
            "TestFilter",
            (filter.Filter,),
            {"foo": fields.Field(field_name="foo", lookup_type="==")},
        )


def test_filter_class_with_meta_model():
    meta = type("Meta", (), {"model": models.Post})
    type(
        "TestFilter",
        (filter.Filter,),
        {"foo": fields.Field(field_name="foo", lookup_type="=="), "Meta": meta},
    )
