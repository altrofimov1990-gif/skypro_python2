import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



class SkyengApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Cookie": f"token_global={token}",
            "Origin": "https://teachers.skyeng.ru",
            "Referer": "https://teachers.skyeng.ru/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
        })

    def create_personal_event(self, title: str, start: str, end: str) -> requests.Response:
        url = f"{self.base_url}/schedule/createPersonal"
        payload = {
            "title": title,
            "startAt": start,
            "endAt": end,
            "description": "",
            "backgroundColor": "#f95313",
            "color": "#020107",
        }
        response = self.session.post(url, json=payload)
        logging.info("Request to %s returned %s: %s", url, response.status_code, response.text[:300])
        return response

    def get_events(self, from_dt: str, till_dt: str) -> requests.Response:
        url = f"{self.base_url}/schedule/events"
        payload = {"from": from_dt, "till": till_dt, "onlyTypes": []}
        response = self.session.post(url, json=payload)
        logging.info("Request to %s returned %s: %s", url, response.status_code, response.text[:300])
        return response

    def delete_event(self, event_id: int, start: str) -> requests.Response:
        """Удаление требует числовой id (payload.id) и startAt события."""
        url = f"{self.base_url}/schedule/removePersonal"
        payload = {"id": event_id, "startAt": start}
        response = self.session.post(url, json=payload)
        logging.info("Request to %s returned %s: %s", url, response.status_code, response.text[:300])
        return response

    @staticmethod
    def extract_event_info(body: dict) -> dict:
        """Возвращает eventId (строковый), числовой id и startAt из ответа на создание."""
        data = body.get("data") or {}
        payload = data.get("payload") or {}
        return {
            "eventId": data.get("eventId"),
            "id": payload.get("id"),
            "startAt": data.get("startAt"),
        }
