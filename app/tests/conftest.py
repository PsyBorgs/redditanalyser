import os.path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from app.database import db as _db
from app.database import create_engine, create_db_session
from app.models import Base


HERE = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_CONFIG = os.path.join(HERE, "..", "..", "alembic.ini")


@pytest.fixture(scope='function')
def db(request):
    """Session-wide test database."""
    # create a SQLite DB in memory
    _db.engine = create_engine("sqlite://")

    # setup models in DB
    Base.metadata.create_all(_db.engine)

    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    return create_db_session(db.engine)
