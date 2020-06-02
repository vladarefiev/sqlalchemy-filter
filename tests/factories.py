import factory

from tests import db, models


class Category(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Category
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u"Category %d" % n)


class Post(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Post
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u"Title %d" % n)
    is_published = True
    category = factory.SubFactory(Category)
