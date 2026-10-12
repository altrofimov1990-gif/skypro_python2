import os

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:12345678@localhost:5432/postgres",
)

TABLE_NAMES = ("students", "subjects", "teachers")


@pytest.fixture(scope="session")
def engine():
    """Единый движок подключения к БД на весь запуск тестов."""
    engine = create_engine(DATABASE_URL)
    yield engine
    engine.dispose()


@pytest.fixture
def tables(engine):
    """Словарь отражённых из БД таблиц учебного проекта."""
    metadata = MetaData()
    metadata.reflect(bind=engine, only=TABLE_NAMES)
    return metadata.tables


@pytest.fixture
def db(engine):
    """Сессия SQLAlchemy с автоочисткой созданных тестом строк."""
    session = sessionmaker(bind=engine)()
    tracked = []

    def track(table, column, value):
        """Запомнить строку, чтобы удалить её после теста."""
        tracked.append((table, column, value))

    yield session, track

    for table, column, value in reversed(tracked):
        session.execute(table.delete().where(getattr(table.c, column) == value))
    session.commit()
    session.close()