# conftest.py
"""Общие фикстуры UI- и API-тестов кабинета учителя Skyeng."""
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterator
from urllib.parse import urlparse

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api_client import SkyengApiClient
from config import API_BASE_URL, TOKEN_GLOBAL
from pages.schedule_page import SchedulePage

logging.basicConfig(level=logging.INFO)

COOKIES_FILE: Path = Path(__file__).parent / "cookies.json"


def _inject_cookies(driver: Any) -> None:
    """Проставляет куки сессии на обоих доменах Skyeng."""
    cookies = json.loads(COOKIES_FILE.read_text("utf-8"))
    added = set()
    for _ in range(2):
        for url in ("https://teachers.skyeng.ru", "https://id.skyeng.ru"):
            try:
                driver.get(url)
            except Exception:  # noqa: BLE001
                pass
            time.sleep(2)
            host = urlparse(driver.current_url).netloc
            for cookie in cookies:
                domain = (cookie.get("domain") or "").lstrip(".")
                if not (domain == host or host.endswith("." + domain)):
                    continue
                key = (cookie["name"], domain)
                if key in added:
                    continue
                try:
                    driver.add_cookie(
                        {
                            k: cookie[k]
                            for k in ("name", "value", "domain", "path")
                            if k in cookie
                        }
                    )
                    added.add(key)
                except Exception:  # noqa: BLE001
                    pass


@pytest.fixture(scope="session")
def api_client() -> SkyengApiClient:
    """Клиент API с сохранённым токеном."""
    return SkyengApiClient(API_BASE_URL, TOKEN_GLOBAL)


@pytest.fixture
def driver() -> Iterator[Any]:
    """Браузер с восстановленной сессией учителя."""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ru")
    driver = webdriver.Chrome(options=options)
    _inject_cookies(driver)
    driver.get("https://teachers.skyeng.ru/schedule")
    time.sleep(5)
    names = [cookie["name"] for cookie in driver.get_cookies()]
    logging.info("Cookies in browser: %s", names)
    logging.info("Current URL: %s", driver.current_url)
    yield driver
    driver.quit()


@pytest.fixture
def schedule_page(driver: Any) -> SchedulePage:
    """Экземпляр страницы расписания."""
    logging.info("Initializing SchedulePage")
    return SchedulePage(driver)


@pytest.fixture
def event(api_client: SkyengApiClient) -> Iterator[Dict[str, Any]]:
    """Создаёт личное событие на сегодня и удаляет его после теста.

    Событие создаётся именно сегодня: календарь по умолчанию
    показывает текущую неделю, а событие «завтра» оставалось
    за пределами видимой области — из-за этого падали детали,
    правка и удаление.
    """
    now = datetime.now().astimezone()
    start = (now + timedelta(hours=2)).replace(
        minute=0, second=0, microsecond=0
    )
    end = start + timedelta(hours=1)
    title = f"Autotest API {uuid.uuid4().hex[:8]}"
    response = api_client.create_personal_event(
        title,
        start.isoformat(timespec="seconds"),
        end.isoformat(timespec="seconds"),
    )
    data: Dict[str, Any] = response.json()["data"]
    event: Dict[str, Any] = {
        "eventId": data["eventId"],
        "id": data["payload"]["id"],
        "startAt": data["startAt"],
        "title": title,
    }
    logging.info(
        "Fixture создала событие: %s (%s)", title, data["eventId"]
    )
    yield event
    api_client.delete_event(event["id"], data["startAt"])
    logging.info("Fixture удалила событие: %s", title)
