import pytest
from sqlalchemy.orm import Query

from sqlalchemy_filter import exceptions, fields, filter, mixins
from tests.models import Post


def test_view_class_with_mixin_without_filter_class():
    with pytest.raises(exceptions.FilterException):
        view_class = type("TestViewClass", (mixins.FilterSetMixin,), {},)
        view_class().filter_query(None, {})


def test_view_class_with_mixin_with_unknown_filter_class():
    with pytest.raises(exceptions.FilterException):
        view_class = type(
            "TestViewClass",
            (mixins.FilterSetMixin,),
            {"filter_class": type("PostFilter", (), {})},
        )
        view_class().filter_query(None, {})


def test_view_class_with_mixin():
    class PostFilter(filter.Filter):
        foo = fields.Field(field_name="foo", lookup_type="==")

        class Meta:
            model = Post

    view_class = type(
        "TestViewClass", (mixins.FilterSetMixin,), {"filter_class": PostFilter},
    )
    query = view_class().filter_query(Post.query, {})
    assert isinstance(query, (Query,))
