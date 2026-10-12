import pytest
from sqlalchemy import select
from db_config import engine, get_session
from models import Base, Student


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def session():
    for s in get_session():
        yield s


@pytest.fixture
def test_student_data():
    return {
        "name": "Test Student",
        "group_name": "TEST-GROUP-001"
    }


def test_add_student(session, test_student_data):
    student = Student(**test_student_data)
    session.add(student)
    session.commit()
    session.refresh(student)

    result = session.execute(
        select(Student).where(Student.id == student.id)
    ).scalar_one_or_none()

    assert result is not None
    assert result.name == test_student_data["name"]
    assert result.group_name == test_student_data["group_name"]

    session.delete(result)
    session.commit()


def test_update_student(session, test_student_data):
    student = Student(**test_student_data)
    session.add(student)
    session.commit()
    session.refresh(student)

    new_group = "UPDATED-GROUP-999"
    student.group_name = new_group
    session.commit()

    updated = session.execute(
        select(Student).where(Student.id == student.id)
    ).scalar_one()

    assert updated.group_name == new_group

    session.delete(updated)
    session.commit()


def test_delete_student(session, test_student_data):
    student = Student(**test_student_data)
    session.add(student)
    session.commit()
    session.refresh(student)

    session.delete(student)
    session.commit()

    result = session.execute(
        select(Student).where(Student.id == student.id)
    ).scalar_one_or_none()

    assert result is None