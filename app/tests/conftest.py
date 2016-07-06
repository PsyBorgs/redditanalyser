import os.path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from app.database import sa, create_engine, create_db_session
from app.models import Base


HERE = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_CONFIG = os.path.join(HERE, "..", "..", "alembic.ini")


def apply_migrations(engine):
    """Applies all alembic migrations."""
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config(ALEMBIC_CONFIG)
    with engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope='session')
def engine(request):
    """Session-wide test database."""
    # create a SQLite DB in memory
    _engine = create_engine("sqlite://")

    # setup models in DB
    Base.metadata.create_all(_engine)

    return _engine


@pytest.fixture(scope='function')
def session(engine, request):
    """Creates a new database session for a test."""
    _session = create_db_session(engine)
    connection = engine.connect()
    transaction = connection.begin()

    def fin():
        transaction.rollback()
        connection.close()

    request.addfinalizer(fin)
    return _session
