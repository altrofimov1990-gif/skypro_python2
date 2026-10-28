import logging
import requests


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

    def delete_event(self, event_id) -> requests.Response:
        url = f"{self.base_url}/schedule/removePersonal"
        response = self.session.post(url, json={"id": event_id})
        logging.info("Request to %s returned %s: %s", url, response.status_code, response.text[:300])
        return response

    @staticmethod
    def extract_event_id(body: dict):
        data = body.get("data") or {}
        return data.get("id") or data.get("eventId")
