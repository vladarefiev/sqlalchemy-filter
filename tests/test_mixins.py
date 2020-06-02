import pytest

from sqlalchemy_filter.mixins import FilterSetMixin
from sqlalchemy_filter.fields import Field
from sqlalchemy_filter.filter import Filter
from tests.models import Post
from sqlalchemy.orm import Query


def test_view_class_with_mixin_bad():
    with pytest.raises(Exception):
        view_class = type("TestViewClass", (FilterSetMixin,), {},)
        view_class().filter_query(None, {})


def test_view_class_with_mixin():
    class PostFilter(Filter):
        foo = Field(field_name="foo", lookup_type="==")

        class Meta:
            model = Post

    view_class = type("TestViewClass", (FilterSetMixin,), {"filter_class": PostFilter},)
    query = view_class().filter_query(Post.query, {})
    assert isinstance(query, (Query,))
