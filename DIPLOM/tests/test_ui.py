# tests/test_ui.py
"""UI-тесты кабинета учителя Skyeng."""
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

import allure
import pytest

from api_client import SkyengApiClient
from pages.schedule_page import SchedulePage


def wide_period() -> Dict[str, str]:
    """Окно ±7 дней: клик по ячейке может попасть в любой видимый день."""
    now: datetime = datetime.now().astimezone()
    return {
        "start": (now - timedelta(days=7)).isoformat(timespec="seconds"),
        "end": (now + timedelta(days=7)).isoformat(timespec="seconds"),
    }


def _window() -> Dict[str, str]:
    """Окно поиска: трое суток назад до недели вперёд."""
    now: datetime = datetime.now().astimezone()
    return {
        "start": (now - timedelta(days=3)).isoformat(timespec="seconds"),
        "end": (now + timedelta(days=7)).isoformat(timespec="seconds"),
    }


def _fetch_events(
    api_client: SkyengApiClient, period: Dict[str, str]
) -> List[Dict[str, Any]]:
    """Забирает список событий за период с проверкой статуса."""
    response = api_client.get_events(period["start"], period["end"])
    if response.status_code != 200:
        logging.warning(
            "get_events ответил %s: %s",
            response.status_code, response.text[:200],
        )
        return []
    body: Dict[str, Any] = response.json().get("data") or {}
    return list(body.get("events") or [])


_TITLE_KEYS = ("title", "name", "subject", "topic")


def _event_title(item: Dict[str, Any]) -> str:
    """Название события.

    Реальная структура ответа: payload.payload.title (двойная
    вложенность payload). Перебирает её и типичные запасные ключи.
    """
    outer = item.get("payload") or {}
    inner = outer.get("payload") or {}
    for key in _TITLE_KEYS:
        value = inner.get(key)
        if value:
            return str(value)
    for key in _TITLE_KEYS:
        value = outer.get(key)
        if value:
            return str(value)
    for key in _TITLE_KEYS:
        value = item.get(key)
        if value:
            return str(value)
    return ""


def dump_event_json(item: Dict[str, Any], label: str) -> None:
    """Печатает полный JSON одного события — для диагностики структуры."""
    logging.info(
        "%s RAW: %s", label, json.dumps(item, ensure_ascii=False)[:1200]
    )


def dump_events(api_client: SkyengApiClient, label: str) -> None:
    """Логирует все события в окне: количество, id, время, название."""
    events = _fetch_events(api_client, _window())
    logging.info("%s: всего событий %d", label, len(events))
    for item in events:
        logging.info(
            "%s: eventId=%s startAt=%s title='%s'",
            label,
            item.get("eventId"),
            item.get("startAt"),
            _event_title(item)[:60],
        )


def find_event_by_id(
    api_client: SkyengApiClient, event_id: str
) -> Optional[Dict[str, Any]]:
    """Ищет событие по eventId в окне вокруг текущего момента."""
    for item in _fetch_events(api_client, _window()):
        if item.get("eventId") == event_id:
            return item
    return None


def wait_for_event(
    api_client: SkyengApiClient,
    event_id: str,
    timeout: int = 30,
) -> Optional[Dict[str, Any]]:
    """Поллит API до появления события с данным eventId."""
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        found = find_event_by_id(api_client, event_id)
        if found is not None:
            logging.info(
                "Событие %s появилось в API через %.0f c ожидания",
                event_id, timeout - (end - time.monotonic()),
            )
            return found
        time.sleep(3)
    return None


def wait_event_gone(
    api_client: SkyengApiClient,
    event_id: str,
    timeout: int = 30,
) -> bool:
    """Поллит API до исчезновения события с данным eventId."""
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if find_event_by_id(api_client, event_id) is None:
            return True
        time.sleep(3)
    return False


class TestSchedule:
    """UI-проверки страницы расписания."""

    @staticmethod
    def _collect_event_ids(
        api_client: SkyengApiClient, period: Dict[str, str]
    ) -> Set[Optional[str]]:
        """Собирает идентификаторы событий за период."""
        return {
            item.get("eventId")
            for item in _fetch_events(api_client, period)
        }

    @allure.title("UI: открытие страницы расписания")
    def test_schedule_page_opens(
        self, schedule_page: SchedulePage
    ) -> None:
        with allure.step("Открыть расписание"):
            schedule_page.open()
        with allure.step("Проверить адрес страницы"):
            assert "teachers.skyeng.ru" in (
                schedule_page.driver.current_url
            ), "Расписание не открылось"

    @allure.title("UI: создание события через интерфейс")
    def test_create_event_via_ui(
        self, schedule_page: SchedulePage, api_client: SkyengApiClient
    ) -> None:
        period: Dict[str, str] = wide_period()
        before: Set[Optional[str]] = self._collect_event_ids(
            api_client, period
        )
        with allure.step("Создать событие через интерфейс"):
            schedule_page.open()
            schedule_page.create_event("Autotest UI")
        with allure.step("Проверить, что событие появилось в API"):
            after: Set[Optional[str]] = self._collect_event_ids(
                api_client, period
            )
            created: Set[Optional[str]] = after - before
            assert created, "Через интерфейс не создано ни одного события"

    @allure.title("UI: открытие карточки события")
    def test_event_details(
        self, schedule_page: SchedulePage, event: Dict[str, Any]
    ) -> None:
        with allure.step("Открыть карточку события"):
            schedule_page.open()
            schedule_page.open_event_details(event["title"])

    @allure.title("UI: редактирование названия события")
    def test_edit_event_title(
        self,
        schedule_page: SchedulePage,
        api_client: SkyengApiClient,
        event: Dict[str, Any],
    ) -> None:
        updated: str = f"{event['title']} edited"
        with allure.step("Проверить видимость события в API до правки"):
            visible = wait_for_event(
                api_client, event["eventId"], timeout=20
            )
            assert visible is not None, (
                "Событие fixture не видно в get_events ещё до правки — "
                "проверочный канал сломан, к UI претензии снимаются"
            )
            before_title = _event_title(visible)
            logging.info(
                "ДО правки: title события %s = '%s' (fixture говорил '%s')",
                event["eventId"], before_title, event["title"],
            )
            assert before_title == event["title"], (
                f"Название до правки не совпадает с fixture: "
                f"в API '{before_title}', ожидалось '{event['title']}'"
            )
        with allure.step("Изменить название через интерфейс"):
            schedule_page.open()
            schedule_page.edit_event_title(event["title"], updated)
        with allure.step("Проверить новое название через API"):

            def _edit_applied() -> Optional[bool]:
                current = find_event_by_id(api_client, event["eventId"])
                if current is None:
                    return None
                title = _event_title(current)
                logging.info(
                    "ПОСЛЕ сохранения: title события %s = '%s'",
                    event["eventId"], title,
                )
                if title == updated:
                    return True
                if title == event["title"]:
                    return None
                return False

            end = time.monotonic() + 30
            result: Optional[bool] = None
            while time.monotonic() < end:
                result = _edit_applied()
                if result is not None:
                    break
                time.sleep(3)
            if result is not True:
                current = find_event_by_id(api_client, event["eventId"])
                if current is not None:
                    dump_event_json(current, "ПОСЛЕ поллинга")
                else:
                    logging.info(
                        "ПОСЛЕ поллинга: событие %s исчезло из выборки",
                        event["eventId"],
                    )
            assert result is True, (
                f"Название не изменилось на '{updated}' "
                f"(итог: {result})"
            )

    @allure.title("UI: удаление события")
    def test_delete_event(
        self,
        schedule_page: SchedulePage,
        api_client: SkyengApiClient,
        event: Dict[str, Any],
    ) -> None:
        with allure.step("Проверить видимость события в API до удаления"):
            visible = wait_for_event(
                api_client, event["eventId"], timeout=20
            )
            assert visible is not None, (
                "Событие fixture не видно в get_events до удаления — "
                "проверка удаления недостоверна"
            )
        with allure.step("Удалить событие через интерфейс"):
            schedule_page.open()
            schedule_page.delete_event(event["title"])
        with allure.step("Проверить, что событие исчезло из API"):
            assert wait_event_gone(
                api_client, event["eventId"], timeout=30
            ), f"Событие {event['eventId']} не удалено из API"
