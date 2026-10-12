"""Тесты добавления, изменения и удаления сущностей учебного проекта."""
import uuid


def _suffix():
    """Уникальный суффикс: тесты можно запускать многократно."""
    return uuid.uuid4().hex[:8]


def _pk(table):
    """Имя первичного ключа таблицы."""
    return list(table.primary_key.columns)[0].name


def test_add_student(db, tables):
    """Добавление студента: строка появляется в таблице students."""
    session, track = db
    students = tables["students"]
    name = f"pytest_student_{_suffix()}"

    result = session.execute(students.insert().values(name=name))
    student_id = result.inserted_primary_key[0]
    track(students, _pk(students), student_id)
    session.commit()

    row = session.execute(
        students.select().where(students.c.id == student_id)
    ).first()
    assert row is not None
    assert row.name == name


def test_update_subject(db, tables):
    """Изменение предмета: заголовок обновляется в таблице subjects."""
    session, track = db
    subjects = tables["subjects"]
    old_title = f"pytest_subject_{_suffix()}"
    new_title = f"pytest_subject_updated_{_suffix()}"

    result = session.execute(subjects.insert().values(title=old_title))
    subject_id = result.inserted_primary_key[0]
    track(subjects, _pk(subjects), subject_id)
    session.commit()

    session.execute(
        subjects.update()
        .where(subjects.c.id == subject_id)
        .values(title=new_title)
    )
    session.commit()

    row = session.execute(
        subjects.select().where(subjects.c.id == subject_id)
    ).first()
    assert row is not None
    assert row.title == new_title


def test_delete_teacher(db, tables):
    """Удаление преподавателя: строка исчезает из таблицы teachers."""
    session, track = db
    teachers = tables["teachers"]
    name = f"pytest_teacher_{_suffix()}"

    result = session.execute(teachers.insert().values(name=name))
    teacher_id = result.inserted_primary_key[0]
    track(teachers, _pk(teachers), teacher_id)
    session.commit()

    session.execute(teachers.delete().where(teachers.c.id == teacher_id))
    session.commit()

    row = session.execute(
        teachers.select().where(teachers.c.id == teacher_id)
    ).first()
    assert row is None