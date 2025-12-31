import pytest
from main import create_app, User, db as _db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def user(db):
    u = User(username="test", email="t@t.com", password_hash="x")
    db.session.add(u)
    db.session.commit()
    return u