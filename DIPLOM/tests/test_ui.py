"""UI-автотесты кабинета учителя Skyeng (Selenium, Page Object)."""
import logging
from typing import Any
from uuid import uuid4

import allure
import pytest

from config import LOGIN, PASSWORD, SKIP_UI_LOGIN
from pages.login_page import LoginPage
from pages.schedule_page import SchedulePage

logging.basicConfig(level=logging.INFO)


class TestLogin:
    @pytest.mark.ui
    @pytest.mark.skipif(SKIP_UI_LOGIN == "true", reason="Форма входа защищена капчей")
    @allure.title("UI: успешная авторизация с валидными данными")
    def test_login_with_valid_credentials(self, driver: Any) -> None:
        page: LoginPage = LoginPage(driver)
        page.open()
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
            assert "schedule" in schedule_page.driver.current_url, \
                "Страница расписания не открылась"

    @pytest.mark.ui
    @allure.title("UI: создание личного события через интерфейс")
    def test_create_event_via_ui(self, schedule_page: SchedulePage) -> None:
        logging.info("Starting test create event via UI")
        title: str = f"Autotest UI {uuid4().hex[:8]}"
        with allure.step("Создать событие через интерфейс"):
            schedule_page.create_event(title)
        with allure.step("Проверить, что событие появилось в расписании"):
            assert schedule_page.has_event(title), \
                f"Событие '{title}' не найдено в расписании"

    @pytest.mark.ui
    @allure.title("UI: просмотр карточки события")
    def test_event_details(self, schedule_page: SchedulePage, ui_event: dict) -> None:
        title: str = ui_event["title"]
        with allure.step("Открыть карточку события"):
            schedule_page.open_event(title)
        with allure.step("Проверить, что карточка события открылась без ошибок"):
            assert schedule_page.has_event(title), \
                f"Карточка события '{title}' не открылась"

    @pytest.mark.ui
    @allure.title("UI: редактирование названия события")
    def test_edit_event_title(self, schedule_page: SchedulePage, ui_event: dict) -> None:
        old_title: str = ui_event["title"]
        new_title: str = f"Autotest UI edited {uuid4().hex[:8]}"
        with allure.step("Открыть карточку события и переименовать"):
            schedule_page.open_event(old_title)
            schedule_page.edit_event_title(old_title, new_title)
        with allure.step("Проверить новое название в расписании"):
            assert schedule_page.has_event(new_title), \
                f"Событие не переименовано в '{new_title}'"

    @pytest.mark.ui
    @allure.title("UI: удаление события")
    def test_delete_event(self, schedule_page: SchedulePage, ui_event: dict) -> None:
        title: str = ui_event["title"]
        with allure.step("Открыть карточку события и удалить"):
            schedule_page.open_event(title)
            schedule_page.delete_event(title)
        with allure.step("Проверить, что событие исчезло из расписания"):
            assert not schedule_page.has_event(title), \
                f"Событие '{title}' всё ещё видно после удаления"