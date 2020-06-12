[![codecov](https://codecov.io/gh/vladarefiev/sqlalchemy-filter/branch/master/graph/badge.svg)](https://codecov.io/gh/vladarefiev/sqlalchemy-filter)

Usage
-----

`sqlalchemy-filter` can be used for generating interfaces similar to the `django-filter`
library. For example, if you have a Post model you can create a
filter for it with the code:

```python
from sqlalchemy_filter import Filter, fields
from app import models

class PostFilter(Filter):
    from_date = fields.DateField(field_name="pub_date", lookup_type=">=")
    to_date = fields.DateField(field_name="pub_date", lookup_type="<=")
    is_published = fields.BooleanField()
    title = fields.Field(lookup_type="==")
    title_like = fields.Field(lookup_type="like")
    title_ilike = fields.Field(lookup_type="ilike")
    data = fields.JsonField(lookup_type="#>>", lookup_path="{foo,0}", not_equal=True)
    category = fields.Field(relation_model="Category", field_name="name", lookup_type="in")
    order = fields.OrderField()

    class Meta:
        model = models.Post
```

And then in your view you could do:

```python
def post_list(request):
    posts = (
        PostFilter()
        .filter_query(Post.query.join(Category), {"category": 'Category 1', 'order': 'title,-id'})
        .all()
    )
    return {"posts": posts}

```    
Above code will perform query like:
```postgresql
SELECT post.id AS post_id, post.title AS post_title, post.pub_date AS post_pub_date, post.is_published AS post_is_published, post.category_id AS post_category_id 
FROM post JOIN category ON category.id = post.category_id 
WHERE category.name IN ('Category 1')
ORDER BY post.title ASC, post.id DESC
```
Notes:
    You should validate your filter params by yourself and pass already validated params to filter_query func, 
    also you should manually make needed joins like in above example ``Post.query.join(Category)``

Possible lookup_types for Field class:

``
['==', '<', '>', '<=', '>=', '!=', 'in', 'not_in', 'like', 'ilike', 'notlike', 'notilike']
``

Possible lookup_types for DateField and DateTimeField class:

``
['==', '<', '>', '<=', '>=', '!=']
``

Possible lookup_types for JsonField class:

``
['->>', '#>>']
``

Examples of usage JsonField:
--------------------------------

```python
from app import models, db

post = models.Post(data={
    "title": "Title 1",
    "is_published": True, 
    "tags": [{"name": "IT"}, {"name": "Biology"}]
})
db.session.add(post)
db.session.commit()
```

```python
from sqlalchemy_filter import fields, Filter
from app import models

class PostFilter(Filter):
    not_title = fields.JsonField(field_name='data', lookup_type='->>', lookup_path='title', not_equal=True)
    is_published = fields.JsonField(field_name='data', lookup_type='->>', lookup_path='is_published')
    tag = fields.JsonField(field_name='data', lookup_type='#>>', lookup_path='{tags, 0, name}')

    class Meta:
        model = models.Post
```

Find posts where title != Title 1

```python
PostFilter().filter_query(models.Post.query, {"not_title": "Title 1"}).all()
```

```postgresql
SELECT *
FROM post 
WHERE (post.data ->> "title") != "Title 1"
```

Find posts where is_published == True

```python
PostFilter().filter_query(models.Post.query, {"is_published": "true"}).all()
```

```postgresql
SELECT *
FROM post 
WHERE (post.data ->> "is_published") = "true"
```

Find posts where first tag name == IT

```python
PostFilter().filter_query(models.Post.query, {"tag": 'IT'}).all()
```

```postgresql
SELECT *
FROM post 
WHERE (post.data #>> "{tags, 0, name}") = "IT"
```

Usage with Flask
--------------------------------

Example below contains integration with Flask:

```python
from flask.views import MethodView
from sqlalchemy_filter.mixins import FilterSetMixin
from app.filters import PostFilter

class PostAPI(MethodView, FilterSetMixin):
    filter_class = PostFilter

    def get(self, *args, **kwargs):
        base_query = Post.query
        filter_params = {...}
        filtered_query = self.filter_query(base_query, filter_params)
        return {"posts": filtered_query.all()}
```
