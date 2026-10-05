"""Тесты метода PUT /api-v2/projects/{id}."""
import uuid


def test_update_project_positive(api, project_id):
    """Переименование существующего проекта."""
    new_title = f"renamed-{uuid.uuid4().hex[:8]}"
    response = api.update(project_id, {"title": new_title})

    assert response.status_code == 200
    assert response.json()["id"] == project_id

    check = api.get(project_id)
    assert check.status_code == 200
    assert check.json()["title"] == new_title


def test_update_project_negative_empty_title(api, project_id):
    """Обновление без обязательного поля title — ошибка 400."""
    response = api.update(project_id, {})

    assert response.status_code == 400
    assert response.json().get("message")


def test_update_project_negative_invalid_id(api):
    """Обновление несуществующего проекта — ошибка 404."""
    response = api.update(
        f"nonexistent-{uuid.uuid4().hex[:8]}", {"title": "x"}
    )

    assert response.status_code == 404
    assert response.json().get("message")