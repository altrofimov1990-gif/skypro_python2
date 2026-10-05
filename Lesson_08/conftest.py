"""Общие фикстуры для автотестов Yougile."""
import uuid

import pytest

from api_client import ProjectPage


@pytest.fixture()
def api():
    return ProjectPage()


@pytest.fixture()
def project_id(api):
    """Создаёт проект и удаляет его после теста (_cleanup)."""
    title = f"autotest-{uuid.uuid4().hex[:8]}"
    response = api.create({"title": title})
    assert response.status_code == 201, "Не удалось создать проект"
    new_id = response.json()["id"]
    yield new_id
    api.delete(new_id)