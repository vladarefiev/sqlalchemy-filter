from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://pylter:password@localhost:5432/pylter"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return f"{self.title}, {self.pub_date}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Category %r>" % self.name


@app.route("/")
def hello_world():
    # db.create_all()
    # db.drop_all()
    # c_1 = Category(name='category 1')
    # c_2 = Category(name='category 2')
    # c_3 = Category(name='category 3')
    # db.session.add_all([
    #     Post(title='title 1', pub_date=datetime(year=2020, month=1, day=1), is_published=False, category=c_1),
    #     Post(title='title 2', pub_date=datetime(year=2020, month=1, day=2), is_published=False, category=c_1),
    #     Post(title='title 3', pub_date=datetime(year=2020, month=1, day=3), category=c_2),
    #     Post(title='title 4', pub_date=datetime(year=2020, month=1, day=4), category=c_2),
    #     Post(title='title 5', pub_date=datetime(year=2020, month=1, day=5), category=c_3),
    # ])
    # db.session.commit()
    # print(Post.query.filter(category.name == 1).all())
    print()
    # Post.query.join(Category).filter(Category.name == 'category 3').all()
    print()
    query = Post.query.join(Category)
    r = None
    print("result:", r)
    return f"Hello, Nastya! {r}"
