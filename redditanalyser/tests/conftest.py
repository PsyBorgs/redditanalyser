from ..database import db as _db


@pytest.yield_fixture(scope='function')
def db():
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.drop_all()
