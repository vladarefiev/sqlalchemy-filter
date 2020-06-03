from unittest import mock

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


@pytest.mark.parametrize(
    "param, called", [("title", True), ("id", False), ("foo", False)],
)
def test_filter_class_with_meta_model(param, called):
    meta = type("Meta", (), {"model": models.Post})
    filter_ = type(
        "TestFilter",
        (filter.Filter,),
        {"title": fields.Field(lookup_type="=="), "Meta": meta},
    )()
    query = mock.Mock()
    filter_.filter_query(query, {param: "some_value"})
    query.filter.assert_called_once() if called else query.filter.assert_not_called()
