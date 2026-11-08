# tests/test_api.py
"""API-тесты расписания кабинета учителя Skyeng."""
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

import allure
import pytest
import requests

from api_client import SkyengApiClient

LOG = logging.getLogger(__name__)

CREATE_URL = "https://api-teachers.skyeng.ru/v2/schedule/createPersonal"

CREATE_CANDIDATES = (
    "create_personal_event", "create_personal", "create_event",
)
REMOVE_CANDIDATES = (
    "remove_personal_event", "remove_personal",
    "delete_personal_event", "remove_event", "delete_event",
)
KWARG_VARIANTS = (
    ("start_at", "end_at"),
    ("startAt", "endAt"),
    ("from_dt", "till_dt"),
    ("from", "till"),
)


def _find_method(
    api_client: SkyengApiClient,
    candidates: tuple,
    purpose: str,
) -> Callable:
    """Ищет метод клиента по списку имён-кандидатов."""
    for name in candidates:
        if hasattr(api_client, name):
            return getattr(api_client, name)
    raise AttributeError(
        f"В SkyengApiClient не найден метод {purpose}: пробовал "
        f"{', '.join(candidates)}"
    )


def _create_personal(
    api_client: SkyengApiClient,
    title: str,
    start_at: str,
    end_at: str,
) -> Any:
    """Создаёт событие, подстраиваясь под реальную сигнатуру клиента."""
    method = _find_method(api_client, CREATE_CANDIDATES, "создания события")
    for start_key, end_key in KWARG_VARIANTS:
        try:
            return method(
                title=title, **{start_key: start_at, end_key: end_at}
            )
        except TypeError:
            continue
    return method(title, start_at, end_at)


def _start_from_event_id(event_id: str) -> Optional[str]:
    """Восстанавливает время начала из составного eventId.

    Формат: S102542401-20261108-110000 — дата и время в UTC.
    Возвращает ISO-строку с зоной, как в ответах API.
    """
    parts = event_id.split("-")
    if len(parts) < 3 or not parts[0].startswith("S"):
        return None
    date_raw, time_raw = parts[1], parts[2]
    if (
        len(date_raw) == 8 and date_raw.isdigit()
        and len(time_raw) == 6 and time_raw.isdigit()
    ):
        return (
            f"{date_raw[0:4]}-{date_raw[4:6]}-{date_raw[6:8]}"
            f"T{time_raw[0:2]}:{time_raw[2:4]}:{time_raw[4:6]}+00:00"
        )
    return None


def _remove_personal(
    api_client: SkyengApiClient,
    event_id: str,
    start_at: Optional[str] = None,
) -> Any:
    """Удаляет событие по сигнатуре клиента.

    API требует числовой идентификатор (payload.id) и время начала.
    Если startAt не передан — восстанавливаем его из eventId, поэтому
    cleanup не падает независимо от точки вызова.
    """
    method = _find_method(api_client, REMOVE_CANDIDATES, "удаления события")
    numeric: Optional[int] = None
    digits = event_id.split("-")[0]
    if digits.startswith("S") and digits[1:].isdigit():
        numeric = int(digits[1:])
    if start_at is None:
        start_at = _start_from_event_id(event_id)
    for candidate_id in (
        (numeric,) if numeric is not None else ()
    ) + (event_id,):
        for extra in (
            ({}, ) if start_at is None else (
                {}, {"start": start_at}, {"start_at": start_at},
                {"startAt": start_at}, {"from": start_at},
            )
        ):
            try:
                return method(candidate_id, **extra)
            except TypeError:
                continue
    return method(event_id)


def _next_round_hour(hours_ahead: int = 2) -> datetime:
    """Ближайший круглый час через заданное число часов от текущего момента."""
    now = datetime.now().astimezone() + timedelta(hours=hours_ahead)
    return now.replace(minute=0, second=0, microsecond=0)


def _fmt(dt: datetime) -> str:
    """Формат дат, который принимает API:
    ГГГГ-ММ-ДДTЧЧ:ММ:СС+ЧЧ:ММ, без микросекунд."""
    return dt.isoformat(timespec="seconds")


def _errors_of(response: Any) -> List[Dict[str, Any]]:
    """Достаёт список ошибок из стандартного конверта ответа."""
    body: Dict[str, Any] = response.json()
    return body.get("errors") or []


def _unauthorized_create(
    api_client: SkyengApiClient,
    title: str,
    start_at: str,
    end_at: str,
) -> Any:
    """Создаёт событие без авторизации прямым запросом.

    Негативная проверка не зависит от внутренней кухни клиента:
    шлём POST без заголовка авторизации и ждём 401.
    """
    return requests.post(
        CREATE_URL,
        json={
            "title": title,
            "startAt": start_at,
            "endAt": end_at,
            "durationSeconds": 3600,
        },
        timeout=30,
    )


class TestCreatePersonalEvent:
    """Проверки создания личного события через API."""

    @allure.title("API: создание события возвращает идентификатор")
    def test_create_event_returns_id(
        self, api_client: SkyengApiClient
    ) -> None:
        start = _next_round_hour()
        end = start + timedelta(hours=1)
        with allure.step("Создать личное событие"):
            response = _create_personal(
                api_client,
                "Autotest API create id",
                _fmt(start),
                _fmt(end),
            )
            assert response.status_code == 200, response.text
            body: Dict[str, Any] = response.json()
            data = body.get("data") or {}
            event_id = data.get("eventId")
            assert event_id, "В ответе нет eventId"
            LOG.info("Создано событие: %s", event_id)
            assert not _errors_of(response), (
                f"API вернул ошибки при создании: {_errors_of(response)}"
            )
        with allure.step("Удалить созданное событие"):
            removed = _remove_personal(
                api_client, event_id, data.get("startAt")
            )
            assert removed.status_code == 200, removed.text
            assert not _errors_of(removed), (
                f"Удаление вернуло ошибки: {_errors_of(removed)}"
            )

    @allure.title("API: создание без токена возвращает 401")
    def test_create_without_token_returns_401(
        self, api_client: SkyengApiClient
    ) -> None:
        start = _next_round_hour()
        end = start + timedelta(hours=1)
        with allure.step("Создать событие без авторизации"):
            response = _unauthorized_create(
                api_client,
                "Autotest API no token",
                _fmt(start),
                _fmt(end),
            )
            assert response.status_code == 401, response.text
            LOG.info("Без токена API ответил 401: %s", response.text[:120])

    @allure.title("API: пустое название отклоняется валидацией")
    def test_create_with_empty_title_is_rejected(
        self, api_client: SkyengApiClient
    ) -> None:
        start = _next_round_hour()
        end = start + timedelta(hours=1)
        with allure.step("Создать событие с пустым названием"):
            response = _create_personal(
                api_client, "", _fmt(start), _fmt(end)
            )
        properties = [
            (error.get("property") or "")
            for error in _errors_of(response)
        ]
        assert "title" in properties, (
            f"Ожидалась ошибка валидации по полю title, получено: "
            f"{properties}"
        )

    @allure.title("API: создание события")
    def test_create_event(
        self, api_client: SkyengApiClient
    ) -> None:
        LOG.info("Starting test create event")
        start = _next_round_hour()
        end = start + timedelta(hours=1)
        event_id: Optional[str] = None
        created_start: Optional[str] = None
        try:
            with allure.step("Создать личное событие"):
                response = _create_personal(
                    api_client,
                    f"Autotest API {int(time.time())}",
                    _fmt(start),
                    _fmt(end),
                )
                assert response.status_code == 200, response.text
                body = response.json()
                data = body.get("data") or {}
                event_id = data.get("eventId")
                created_start = data.get("startAt")
                assert event_id, "Событие не создано"
            with allure.step("Проверить эхо времени начала"):
                returned = created_start or ""
                assert returned, "В ответе нет startAt"
                moment_sent = datetime.fromisoformat(_fmt(start))
                moment_got = datetime.fromisoformat(returned)
                assert moment_sent == moment_got, (
                    f"startAt в ответе не совпал с отправленным: "
                    f"отправлено {_fmt(start)}, получено {returned}"
                )
        finally:
            if event_id:
                _remove_personal(api_client, event_id, created_start)

    @allure.title("API: конец раньше начала отклоняется")
    def test_create_end_before_start_is_rejected(
        self, api_client: SkyengApiClient
    ) -> None:
        start = _next_round_hour()
        end = start + timedelta(hours=1)
        with allure.step("Создать событие с endAt раньше startAt"):
            response = _create_personal(
                api_client,
                "Autotest API wrong order",
                _fmt(end),
                _fmt(start),
            )
        properties = [
            (error.get("property") or "")
            for error in _errors_of(response)
        ]
        codes = [
            ((error.get("error") or {}).get("code") or "")
            for error in _errors_of(response)
        ]
        assert "startAt" in properties and "domain_error" in codes, (
            f"Ожидалась domain_error по startAt, получено: "
            f"properties={properties}, codes={codes}"
        )


class TestGetEvents:
    """Проверки получения списка событий."""

    @allure.title("API: созданное событие присутствует в списке за период")
    def test_created_event_in_list(
        self, api_client: SkyengApiClient, event: Dict[str, Any]
    ) -> None:
        with allure.step("Запросить расписание на период события"):
            start = datetime.fromisoformat(event["startAt"])
            from_dt = (start - timedelta(days=1)).isoformat(
                timespec="seconds"
            )
            till_dt = (start + timedelta(days=1)).isoformat(
                timespec="seconds"
            )
        with allure.step("Найти событие в списке по eventId"):
            found: Optional[Dict[str, Any]] = None
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                response = api_client.get_events(from_dt, till_dt)
                events = (
                    (response.json().get("data") or {}).get("events")
                    or []
                )
                for item in events:
                    if item.get("eventId") == event["eventId"]:
                        found = item
                        break
                if found is not None:
                    break
                time.sleep(3)
            assert found is not None, (
                f"Событие {event['eventId']} не появилось в списке "
                f"get_events за 20 секунд"
            )
            LOG.info(
                "Событие найдено в списке: %s", found.get("eventId")
            )
