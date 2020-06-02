Usage
-----

`sqlalchemy-filter` can be used for generating interfaces similar to the `django-filter`
library. For example, if you had a Post model you could have a
filter for it with the code:

```python
    from sqlalchemy_filter import Filter

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
```

And then in your view you could do:

```python
    def post_list(request):
        posts = (
            PostFilter()
            .filter_query(Post.query.join(Category), {"category": 'Category 1'})
            .all()
        )
        return {"posts": posts}

```    
Above code will perform query like:
```sql
    SELECT post.id AS post_id, post.title AS post_title, post.pub_date AS post_pub_date, post.is_published AS post_is_published, post.category_id AS post_category_id 
    FROM post JOIN category ON category.id = post.category_id 
    WHERE category.name IN (%(name_1)s)
```
Notes:
    You should validate your filter params by yourself and pass already validated params to filter_query func, 
    also you should manually make needed joins like in above example ``Post.query.join(Category)``

Usage with Flask
--------------------------------

Example below contains integration with Flask:

```python
    
    from flask.views import MethodView
    from sqlalchemy_filter.mixins import FilterSetMixin
    
    class PostAPI(MethodView, FilterSetMixin):
        filter_class = PostFilter

        def get(self, *args, **kwargs):
            base_query = Post.query
            filter_params = {...}
            filtered_query = self.filter_query(base_query, filter_params)
            return {"posts": filtered_query.all()}
```
