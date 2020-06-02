import os

import pytest
from flask import Flask

from tests import db


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://{user}:{password}@{host}:5432/{db}".format(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        db=os.environ["POSTGRES_DB"],
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    return app


@pytest.fixture(autouse=True)
def database(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app
        db.session.close()
        db.drop_all()
