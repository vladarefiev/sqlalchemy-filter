import pytest

from sqlalchemy_filter.fields import Field
from sqlalchemy_filter.filter import BaseFilter, FilterSetMixin

from tests.models import Post


def test_base_filter_class():
    with pytest.raises(TypeError):
        BaseFilter()


def test_filter_class_without_meta_model():
    with pytest.raises(Exception):
        type(
            "TestFilter",
            (BaseFilter,),
            {"foo": Field(field_name="foo", lookup_type="==")},
        )


def test_view_class_with_mixin_bad():
    with pytest.raises(Exception):
        view_class = type("TestViewClass", (FilterSetMixin,), {},)
        view_class().filter_query(None, {})


def test_view_class_with_mixin():
    class Filter(BaseFilter):
        foo = Field(field_name="foo", lookup_type="==")

        class Meta:
            model = Post

    view_class = type("TestViewClass", (FilterSetMixin,), {"filter_class": Filter},)
    view_class().filter_query(None, {})
