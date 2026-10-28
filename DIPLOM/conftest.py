# conftest.py
import logging
from typing import Any, Dict, Iterator
from uuid import uuid4

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api_client import SkyengApiClient
from config import API_BASE_URL, BASE_URL, COOKIE_DOMAIN, HEADLESS, TOKEN_GLOBAL
from data_utils import next_day_period
from pages.schedule_page import SchedulePage

logging.basicConfig(level=logging.INFO)


def pytest_configure(config):
    config.addinivalue_line("markers", "api: mark test as api test")
    config.addinivalue_line("markers", "ui: mark test as ui test")


@pytest.fixture
def driver() -> Iterator[webdriver.Chrome]:
    with allure.step("Запуск браузера Chrome"):
        options = Options()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--lang=ru")
        driver = webdriver.Chrome(options=options)
        driver.get(BASE_URL)
        driver.add_cookie({
            "name": "token_global",
            "value": TOKEN_GLOBAL,
            "domain": COOKIE_DOMAIN,
        })
    yield driver
    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.fixture
def schedule_page(driver: webdriver.Chrome) -> SchedulePage:
    logging.info("Initializing SchedulePage")
    return SchedulePage(driver)


@pytest.fixture
def api_client() -> SkyengApiClient:
    return SkyengApiClient(API_BASE_URL, TOKEN_GLOBAL)


@pytest.fixture
def ui_event(schedule_page: SchedulePage) -> Iterator[Dict[str, Any]]:
    """Создаёт событие через интерфейс и удаляет его после теста."""
    title: str = f"Autotest UI {uuid4().hex[:8]}"
    with allure.step("Подготовка: создание события через интерфейс"):
        schedule_page.open()
        schedule_page.create_event(title)
    yield {"title": title}
    with allure.step("Очистка: удаление события через интерфейс"):
        try:
            schedule_page.open()
            schedule_page.delete_event(title)
        except Exception as e:
            logging.warning("Не удалось удалить тестовое событие '%s': %s", title, e)


@pytest.fixture
def event(api_client: SkyengApiClient) -> Iterator[Dict[str, Any]]:
    """Создаёт уникальное событие через API и удаляет его после теста."""
    period: Dict[str, str] = next_day_period()
    title: str = f"Autotest API {uuid4().hex[:8]}"
    with allure.step("Подготовка: создание события через API"):
        response = api_client.create_personal_event(title, period["start"], period["end"])
        try:
            assert response.status_code == 200, (
                f"Создание события вернуло {response.status_code}: {response.text[:300]}"
            )
        except AssertionError as e:
            print("Ошибка создания события:", response.text)
            raise e
        body: Dict[str, Any] = response.json()
        event_id = SkyengApiClient.extract_event_id(body)
        assert event_id is not None, f"В ответе нет id события: {body}"
    yield {"id": event_id, "title": title, "period": period}
    with allure.step("Очистка: удаление события"):
        api_client.delete_event(event_id)