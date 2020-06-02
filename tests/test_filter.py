import pytest

from sqlalchemy_filter.fields import Field
from sqlalchemy_filter.filter import Filter


def test_base_filter_class():
    with pytest.raises(TypeError):
        Filter()


def test_filter_class_without_meta_model():
    with pytest.raises(Exception):
        type(
            "TestFilter", (Filter,), {"foo": Field(field_name="foo", lookup_type="==")},
        )
