"""API-автотесты расписания кабинета учителя Skyeng."""
from typing import Any, Dict
from uuid import uuid4

import allure
import pytest

from api_client import SkyengApiClient
from config import API_BASE_URL
from data_utils import next_day_period


@pytest.mark.api
@allure.story("Создание личного события")
class TestCreatePersonalEvent:

    @allure.title("API: создание личного события с валидными данными возвращает id")
    def test_create_event_returns_id(self, api_client: SkyengApiClient) -> None:
        period: Dict[str, str] = next_day_period()
        title: str = f"Autotest API {uuid4().hex[:8]}"
        with allure.step("Отправить запрос на создание личного события"):
            response = api_client.create_personal_event(
                title, period["start"], period["end"]
            )
        with allure.step("Проверить статус-код и наличие id в ответе"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
            event_id = SkyengApiClient.extract_event_id(response.json())
            assert event_id is not None, "id события отсутствует в ответе"
        with allure.step("Очистка данных: удалить созданное событие"):
            api_client.delete_event(event_id)

    @allure.title("API: запрос без токена возвращает 401")
    def test_create_without_token_returns_401(self) -> None:
        period: Dict[str, str] = next_day_period()
        client = SkyengApiClient(API_BASE_URL, "")
        with allure.step("Отправить запрос без Cookie token_global"):
            response = client.create_personal_event(
                "No auth test", period["start"], period["end"]
            )
        with allure.step("Проверить статус-код 401"):
            assert response.status_code == 401, \
                f"Ожидался 401, получен {response.status_code}"

    @allure.title("API: пустое название события отклоняется валидацией")
    def test_create_with_empty_title_is_rejected(self, api_client: SkyengApiClient) -> None:
        period: Dict[str, str] = next_day_period()
        with allure.step("Отправить запрос с пустым title"):
            response = api_client.create_personal_event(
                "", period["start"], period["end"]
            )
        with allure.step("Проверить ошибку валидации"):
            assert 400 <= response.status_code < 500, \
                f"Ожидался 4xx, получен {response.status_code}"
            body: Dict[str, Any] = response.json()
            assert body.get("errors"), "Ожидали ошибку в конверте, получили errors=null"

    @allure.title("API: событие с концом раньше начала отклоняется валидацией")
    def test_create_end_before_start_is_rejected(self, api_client: SkyengApiClient) -> None:
        period: Dict[str, str] = next_day_period()
        with allure.step("Отправить запрос, где endAt раньше startAt"):
            response = api_client.create_personal_event(
                "Backwards time", period["end"], period["start"]
            )
        with allure.step("Проверить ошибку валидации времени"):
            assert 400 <= response.status_code < 500, \
                f"Ожидался 4xx, получен {response.status_code}"
            body = response.json()
            assert body.get("errors") or body.get("message"), "В ответе нет описания ошибки"


@pytest.mark.api
@allure.story("Просмотр расписания")
class TestGetEvents:

    @allure.title("API: созданное событие присутствует в списке за период")
    def test_created_event_in_list(self, api_client: SkyengApiClient,
                                  event: Dict[str, Any]) -> None:
        period: Dict