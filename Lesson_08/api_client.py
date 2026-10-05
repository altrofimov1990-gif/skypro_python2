"""PageObject для работы с методами Yougile по проектам."""
import os

import requests

BASE_URL = os.getenv("YOUGILE_URL", "https://ru.yougile.com/api-v2")
TOKEN = os.environ["API_TOKEN"]


class ProjectPage:
    """Обёртка над API-методами раздела projects."""

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }

    def create(self, payload):
        """POST /api-v2/projects — создание проекта."""
        return requests.post(
            f"{BASE_URL}/projects", json=payload, headers=self.headers
        )

    def get(self, project_id):
        """GET /api-v2/projects/{id} — получение проекта по id."""
        return requests.get(
            f"{BASE_URL}/projects/{project_id}", headers=self.headers
        )

    def update(self, project_id, payload):
        """PUT /api-v2/projects/{id} — обновление или удаление."""
        return requests.put(
            f"{BASE_URL}/projects/{project_id}",
            json=payload,
            headers=self.headers,
        )

    def delete(self, project_id):
        """Мягкое удаление проекта: PUT с флагом deleted=True."""
        return self.update(project_id, {"deleted": True})