"""UI-автотесты кабинета учителя Skyeng (Selenium, Page Object)."""
import os
import time
from typing import Any
from uuid import uuid4

import allure
import pytest

from api_client import SkyengApiClient
from config import LOGIN, PASSWORD, SKIP_UI_LOGIN
from pages.login_page import LoginPage
from pages.schedule_page import SchedulePage

requires_api = pytest.mark.skipif(
    os.getenv("API_READY", "false") != "true",
    reason="Ждём подтверждённый эндпоинт создания события из DevTools",
)


class TestLogin:
    @pytest.mark.ui
    @pytest.mark.skipif(SKIP_UI_LOGIN == "true", reason="Форма входа защищена капчей")
    @allure.title("UI: успешная авторизация с валидными данными")
    def test_login_with_valid_credentials(self, driver: Any) -> None:
        page: LoginPage = LoginPage(driver)
        page.open()
        time.sleep(3)
        page.login(LOGIN, PASSWORD)
        with allure.step("Проверить, что выполнен вход в кабинет"):
            assert page.is_logged_in(), (
                f"После входа URL не покинул страницу логина: {driver.current_url}"
            )


class TestSchedule:
    @pytest.mark.ui
    @allure.title("UI: страница расписания открывается")
    def test_schedule_page_opens(self, schedule_page: SchedulePage) -> None:
        with allure.step("Открыть страницу расписания"):
            schedule_page.open()
        with allure.step("Проверить, что страница загрузилась"):
            assert "schedule" in schedule_page.driver.current_url or \
                schedule_page.is_page_loaded(), "Страница расписания не открылась"

    @pytest.mark.ui
    @requires_api
    @allure.title("UI: создание личного события через интерфейс")
    def test_create_event_via_ui(self, schedule_page: SchedulePage,
                                 api_client: SkyengApiClient) -> None:
        from data_utils import next_day_period
        period = next_day_period()
        title: str = f"Autotest UI {uuid4().hex[:8]}"
        with allure.step("Создать событие через интерфейс"):
            schedule_page.create_event(title)
        with allure.step("Проверить, что событие появилось в расписании"):
            assert schedule_page.is_event_visible(title), \
                f"Событие '{title}' не найдено в расписании"

    @pytest.mark.ui
    @requires_api
    @allure.title("UI: просмотр деталей события")
    def test_event_details(self, schedule_page: SchedulePage,
                           event: dict) -> None:
        with allure.step("Открыть карточку события"):
            schedule_page.open_event(event["title"])
        with allure.step("Проверить название события в карточке"):
            assert event["title"] in schedule_page.get_event_details_title()

    @pytest.mark.ui
    @requires_api
    @allure.title("UI: редактирование названия события")
    def test_edit_event_title(self, schedule_page: SchedulePage,
                              event: dict) -> None:
        new_title: str = f"Autotest UI edited {uuid4().hex[:8]}"
        with allure.step("Открыть карточку события и переименовать"):
            schedule_page.open_event(event["title"])
            schedule_page.edit_event(new_title)
        with allure.step("Проверить новое название в расписании"):
            assert schedule_page.is_event_visible(new_title), \
                f"Событие не переименовано в '{new_title}'"

    @pytest.mark.ui
    @requires_api
    @allure.title("UI: удаление события")
    def test_delete_event(self, schedule_page: SchedulePage,
                          event: dict) -> None:
        with allure.step("Открыть карточку события и удалить"):
            schedule_page.open_event(event["title"])
            schedule_page.delete_event()
        with allure.step("Проверить, что событие исчезло из расписания"):
            assert not schedule_page.is_event_visible(event["title"]), \
                f"Событие '{event['title']}' всё ещё видно после удаления"