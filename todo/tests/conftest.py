import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import models


@pytest.fixture()
def test_db(tmp_path_factory) -> Session:
    SQLALCHEMY_DATABASE_URL = "sqlite:///" + \
        str(tmp_path_factory.mktemp("sqlitedb")) + "/todo.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    models.Base.metadata.create_all(bind=engine)

    return SessionLocal()
