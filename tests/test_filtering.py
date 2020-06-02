from datetime import datetime, date
import pytest

from sqlalchemy_filter.fields import BooleanField, Field
from sqlalchemy_filter.filter import Filter
from tests import factories
from tests.models import Category, Post


class PostFilter(Filter):
    from_date = Field(field_name="pub_date", lookup_type=">=")
    to_date = Field(field_name="pub_date", lookup_type="<=")
    is_published = BooleanField(field_name="is_published")
    title = Field(field_name="title", lookup_type="==")
    title_like = Field(field_name="title", lookup_type="like")
    title_ilike = Field(field_name="title", lookup_type="ilike")
    category = Field(relation_model="Category", field_name="name", lookup_type="in")

    class Meta:
        model = Post


def test_filter_from_date(database):
    factories.Post.create(pub_date=datetime(year=2020, month=1, day=1))
    post = factories.Post.create(pub_date=datetime(year=2020, month=1, day=2))
    query = PostFilter().filter_query(Post.query, {"from_date": "2020-01-02"}).all()
    assert len(query) == 1
    assert query[0].id == post.id


@pytest.mark.parametrize(
    "to_date_param", [(date(year=2020, month=1, day=1),), ("2020-01-01",)]
)
def test_filter_to_date_datetime(database, to_date_param):
    post = factories.Post.create(pub_date=datetime(year=2020, month=1, day=1))
    factories.Post.create(pub_date=datetime(year=2020, month=10, day=2))
    query = PostFilter().filter_query(Post.query, {"to_date": to_date_param}).all()
    assert len(query) == 1
    assert query[0].id == post.id


def test_filter_is_published(database):
    post = factories.Post.create(is_published=True)
    factories.Post.create(is_published=False)
    query = PostFilter().filter_query(Post.query, {"is_published": True}).all()
    assert len(query) == 1
    assert query[0].id == post.id


def test_filter_title(database):
    post = factories.Post.create(title="1")
    factories.Post.create(title="2")
    query = PostFilter().filter_query(Post.query, {"title": post.title}).all()
    assert len(query) == 1
    assert query[0].id == post.id


def test_filter_category(database):
    category_1 = factories.Category.create(name="1")
    category_2 = factories.Category.create(name="2")
    post = factories.Post.create(title="1", category=category_1)
    factories.Post.create(title="2", category=category_2)
    query = (
        PostFilter()
        .filter_query(Post.query.join(Category), {"category": category_1.name})
        .all()
    )
    assert len(query) == 1
    assert query[0].id == post.id
