import requests
from typing import Any, Dict, Optional
from datetime import datetime

class SkyengApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()  # Добавляем создание сессии
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        })

    def create_personal_event(
        self, 
        title: str, 
        start: str, 
        end: str
    ) -> requests.Response:
        url = f"{self.base_url}/events"
        payload = {
            "title": title,
            "startAt": start,
            "endAt": end
        }
        return self.session.post(url, json=payload)

    def delete_event(self, event_id: int) -> requests.Response:
        url = f"{self.base_url}/events/{event_id}"
        return self.session.delete(url)

    @staticmethod
    def extract_event_id(response_data: Dict[str, Any]) -> Optional[int]:
        return response_data.get('id')

    def get_events(self) -> requests.Response:
        url = f"{self.base_url}/events"
        return self.session.get(url)