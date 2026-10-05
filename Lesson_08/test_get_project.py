"""Тесты метода GET /api-v2/projects/{id}."""
import uuid


def test_get_project_positive(api, project_id):
    """Получение существующего проекта по id."""
    response = api.get(project_id)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == project_id
    assert "title" in body
    assert body.get("deleted") is False


def test_get_project_negative_invalid_id(api):
    """Запрос несуществующего проекта — ошибка 404."""
    response = api.get(f"nonexistent-{uuid.uuid4().hex[:8]}")

    assert response.status_code == 404
    assert response.json().get("message")