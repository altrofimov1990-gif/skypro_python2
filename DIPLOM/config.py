"""Конфигурация проекта. Значения берутся из .env — в коде нет секретов."""
import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

BASE_URL: Final[str] = os.getenv("BASE_URL", "https://teachers.skyeng.ru")
API_BASE_URL = "https://api-teachers.skyeng.ru/v2"
LOGIN: Final[str] = os.getenv("LOGIN", "")
PASSWORD: Final[str] = os.getenv("PASSWORD", "")
TOKEN_GLOBAL: Final[str] = os.getenv("TOKEN_GLOBAL", "")
COOKIE_DOMAIN: Final[str] = os.getenv("COOKIE_DOMAIN", ".skyeng.ru")
HEADLESS: Final[bool] = os.getenv("HEADLESS", "true").lower() == "true"
SKIP_UI_LOGIN: Final[str] = os.getenv("SKIP_UI_LOGIN", "false")
SCHEDULE_PATH: Final[str] = "/schedule"
AUTH_CODE: str = os.getenv("AUTH_CODE", "")
TEACHER_ID: str = os.getenv("TEACHER_ID", "")