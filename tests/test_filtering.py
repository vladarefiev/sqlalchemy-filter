from datetime import date, datetime

import pytest

from sqlalchemy_filter import fields, filter
from tests import factories, models


class PostFilter(filter.Filter):
    from_date = fields.Field(field_name="pub_date", lookup_type=">=")
    to_date = fields.Field(field_name="pub_date", lookup_type="<=")
    is_published = fields.BooleanField()
    title = fields.Field(lookup_type="==")
    title_like = fields.Field(lookup_type="like")
    title_ilike = fields.Field(lookup_type="ilike")
    category = fields.Field(
        relation_model="Category", field_name="name", lookup_type="in"
    )

    class Meta:
        model = models.Post


@pytest.mark.parametrize(
    "to_date_param", [(date(year=2020, month=1, day=2),), ("2020-01-02",)]
)
def test_filter_from_date(database, to_date_param):
    factories.Post.create(pub_date=datetime(year=2020, month=1, day=1))
    post = factories.Post.create(pub_date=datetime(year=2020, month=1, day=2))
    result = (
        PostFilter().filter_query(models.Post.query, {"from_date": to_date_param}).all()
    )
    assert len(result) == 1
    assert result[0].id == post.id


@pytest.mark.parametrize(
    "to_date_param", [(date(year=2020, month=1, day=1),), ("2020-01-01",)]
)
def test_filter_to_date_datetime(database, to_date_param):
    post = factories.Post.create(pub_date=datetime(year=2020, month=1, day=1))
    factories.Post.create(pub_date=datetime(year=2020, month=10, day=2))
    result = (
        PostFilter().filter_query(models.Post.query, {"to_date": to_date_param}).all()
    )
    assert len(result) == 1
    assert result[0].id == post.id


def test_filter_is_published(database):
    post = factories.Post.create(is_published=True)
    factories.Post.create(is_published=False)
    result = PostFilter().filter_query(models.Post.query, {"is_published": True}).all()
    assert len(result) == 1
    assert result[0].id == post.id


def test_filter_title(database):
    post = factories.Post.create(title="1")
    factories.Post.create(title="2")
    result = PostFilter().filter_query(models.Post.query, {"title": post.title}).all()
    assert len(result) == 1
    assert result[0].id == post.id


def test_filter_category(database):
    category_1 = factories.Category.create(name="1")
    category_2 = factories.Category.create(name="2")
    post = factories.Post.create(title="1", category=category_1)
    factories.Post.create(title="2", category=category_2)
    result = (
        PostFilter()
        .filter_query(
            models.Post.query.join(models.Category), {"category": category_1.name}
        )
        .all()
    )
    assert len(result) == 1
    assert result[0].id == post.id


@pytest.mark.parametrize(
    "lookup_type, lookup_path, param, not_equal, expected_id",
    [
        ("->>", "field_1", "1", False, 1),
        ("->>", "field_1", "5", False, 2),
        ("#>>", "{field_1}", "5", False, 2),
        ("#>>", "{field_3, field_2}", "2", False, 1),
        ("#>>", "{field_3, field_2}", "2", True, 2),
        ("#>>", "{field_3, field_3, field_1}", "1", False, 1),
        ("#>>", "{field_2, 0}", "1", False, 2),
    ],
)
def test_filter_jsonb(
    database, lookup_type, lookup_path, param, not_equal, expected_id
):
    meta = type("Meta", (), {"model": models.Post})
    json_filter = type(
        "JsonPostFilter",
        (PostFilter,),
        {
            "data": fields.JsonField(
                lookup_type=lookup_type, lookup_path=lookup_path, not_equal=not_equal
            ),
            "Meta": meta,
        },
    )()
    factories.Post.create(
        id=1,
        data={
            "field_1": 1,
            "field_2": 2,
            "field_3": {
                "field_1": 1,
                "field_2": 2,
                "field_3": {"field_1": 1, "field_2": 2},
            },
        },
    )
    factories.Post.create(
        id=2,
        data={
            "field_1": 5,
            "field_2": [1, 2, 3],
            "field_3": {
                "field_1": 5,
                "field_2": 6,
                "field_3": {"field_1": 5, "field_2": 6},
            },
        },
    )
    result = json_filter.filter_query(models.Post.query, {"data": param}).all()
    assert len(result) == 1
    assert result[0].id == expected_id
