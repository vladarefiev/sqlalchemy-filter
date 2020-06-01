from datetime import datetime

from sqlalchemy_filter.fields import BooleanField, Field
from sqlalchemy_filter.filter import BaseFilter
from tests import db
from tests.models import Category, Post


class Filter(BaseFilter):
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
    post_1 = Post(title="1", pub_date=datetime(year=2020, month=1, day=1))
    post_2 = Post(title="2", pub_date=datetime(year=2020, month=1, day=2))
    db.session.add_all([post_1, post_2])
    db.session.commit()
    query = Filter().filter_query(Post.query, {"from_date": "2020-01-02"}).all()
    assert len(query) == 1
    assert query[0].id == post_2.id


def test_filter_to_date_datetime(database):
    post_1 = Post(title="1", pub_date=datetime(year=2020, month=1, day=1))
    post_2 = Post(title="2", pub_date=datetime(year=2020, month=10, day=2))
    db.session.add_all([post_1, post_2])
    db.session.commit()
    query = Filter().filter_query(Post.query, {"to_date": datetime.today()}).all()
    assert len(query) == 1
    assert query[0].id == post_1.id


def test_filter_to_date_str(database):
    post_1 = Post(title="1", pub_date=datetime(year=2020, month=1, day=1))
    post_2 = Post(title="2", pub_date=datetime(year=2020, month=1, day=2))
    db.session.add_all([post_1, post_2])
    db.session.commit()
    query = Filter().filter_query(Post.query, {"to_date": "2020-01-01"}).all()
    assert len(query) == 1
    assert query[0].id == post_1.id


def test_filter_is_published(database):
    post_1 = Post(title="1", is_published=True)
    post_2 = Post(title="1", is_published=False)
    db.session.add_all([post_1, post_2])
    db.session.commit()
    query = Filter().filter_query(Post.query, {"is_published": True}).all()
    assert len(query) == 1
    assert query[0].id == post_1.id


def test_filter_title(database):
    post_1 = Post(title="1")
    post_2 = Post(title="2")
    db.session.add_all([post_1, post_2])
    db.session.commit()
    query = Filter().filter_query(Post.query, {"title": post_1.title}).all()
    assert len(query) == 1
    assert query[0].id == post_1.id


def test_filter_category(database):
    category_1 = Category(name="1")
    category_2 = Category(name="2")
    post_1 = Post(title="1", category=category_1)
    post_2 = Post(title="2", category=category_2)
    db.session.add_all([post_1, post_2, category_1, category_2])
    db.session.commit()
    query = (
        Filter()
        .filter_query(Post.query.join(Category), {"category": category_1.name})
        .all()
    )
    assert len(query) == 1
    assert query[0].id == post_1.id
