import pytest

from sqlalchemy_filter import filter, fields


def test_base_filter_class():
    with pytest.raises(TypeError):
        filter.Filter()


def test_filter_class_without_meta_model():
    with pytest.raises(Exception):
        type(
            "TestFilter",
            (filter.Filter,),
            {"foo": fields.Field(field_name="foo", lookup_type="==")},
        )
