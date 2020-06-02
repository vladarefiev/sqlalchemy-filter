import pytest
from sqlalchemy.orm import Query

from sqlalchemy_filter import fields, filter, mixins
from tests.models import Post


def test_view_class_with_mixin_bad():
    with pytest.raises(Exception):
        view_class = type("TestViewClass", (mixins.FilterSetMixin,), {},)
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
