"""Клиент API расписания кабинета учителя Skyeng (api-teachers.skyeng.ru/v2)."""
from typing import Any, Dict, Optional

import requests

DEFAULT_COLORS: Dict[str, str] = {
    "backgroundColor": "#F4F5F6",
    "color": "#81888D",
}


class SkyengApiClient:
    def __init__(self, base_url: str, token: str, timeout: int = 30) -> None:
        self.base_url: str = base_url.rstrip("/")
        self.token: str = token
        self.timeout: int = timeout
        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://teachers.skyeng.ru",
            "Referer": "https://teachers.skyeng.ru/",
        })

    def _auth_cookies(self) -> Dict[str, str]:
        return {"token_global": self.token} if self.token else {}

    def create_personal_event(self, title: str, start_at: str, end_at: str,
                              description: str = "") -> requests.Response:
        return self.session.post(
            f"{self.base_url}/schedule/createPersonal",
            json={
                "title": title,
                "description": description,
                "startAt": start_at,
                "endAt": end_at,
                **DEFAULT_COLORS,
            },
            cookies=self._auth_cookies(),
            timeout=self.timeout,
        )

    def get_events(self, from_at: str, till_at: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/schedule/events",
            json={"from": from_at, "till": till_at},
            cookies=self._auth_cookies(),
            timeout=self.timeout,
        )

    def delete_event(self, event_id: int) -> requests.Response:
        # TODO: путь удаления уточнить по cURL из DevTools
        return self.session.post(
            f"{self.base_url}/schedule/deletePersonal",
            json={"eventId": int(event_id)},
            cookies=self._auth_cookies(),
            timeout=self.timeout,
        )

    @staticmethod
    def extract_event_id(response_json: Dict[str, Any]) -> Optional[int]:
        try:
            return int(response_json["data"]["payload"]["id"])
        except (KeyError, TypeError, ValueError):
            return None

    @staticmethod
    def find_event_in_list(events_json: Dict[str, Any], title: str) -> Optional[Dict[str, Any]]:
        for item in events_json.get("data", []):
            if isinstance(item, dict) and item.get("payload", {}).get("payload", {}).get("title") == title:
                return item
        return None