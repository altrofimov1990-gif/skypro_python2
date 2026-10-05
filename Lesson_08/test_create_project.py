"""Тесты метода POST /api-v2/projects."""
import uuid

from api_client import ProjectPage


def test_create_project_positive(api):
    """Создание проекта с корректным названием."""
    title = f"autotest-{uuid.uuid4().hex[:8]}"
    response = api.create({"title": title})

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    project_page = ProjectPage()
    project_page.delete(body["id"])


def test_create_project_negative_empty_title(api):
    """Создание без обязательного поля title — ошибка 400."""
    response = api.create({})

    assert response.status_code == 400
    assert response.json().get("message")


def test_create_project_negative_no_auth():
    """Запрос без токена — ошибка 401."""
    import requests

    response = requests.post(
        "https://ru.yougile.com/api-v2/projects", json={"title": "x"}
    )

    assert response.status_code == 401
    assert response.json().get("message")