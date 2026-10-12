"""Подключение к учебной базе данных."""
from sqlalchemy import MetaData, create_engine

from conftest import DATABASE_URL

DATABASE_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/postgres"

def create_db_engine():
    """Создать движок подключения к локальной БД."""
    return create_engine(DATABASE_URL)


def get_tables(engine):
    """Отразить таблицы учебного проекта и вернуть их словарём."""
    metadata = MetaData()
    metadata.reflect(bind=engine, only=("students", "subjects", "teachers"))
    return metadata.tables