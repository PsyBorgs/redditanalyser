import pytest

from ..database import create_db_session


@pytest.yield_fixture(scope='function')
def db():
    _db = create_db_session('sqlite://')

    yield _db

    _db.drop_all()
