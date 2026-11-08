# login_save.py
"""Ручной вход в кабинет и сохранение кук сессии в cookies.json."""
import json
import time
from typing import Any, Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LOGIN_URL: str = (
    "https://id.skyeng.ru/login"
    "?redirect=https%3A%2F%2Fteachers.skyeng.ru"
)
CABINET_URL: str = "https://teachers.skyeng.ru"
ID_URL: str = "https://id.skyeng.ru"
COOKIES_FILE: str = "cookies.json"
WAIT_SECONDS: int = 600


def safe_current_url(driver: webdriver.Chrome) -> str:
    """Возвращает текущий URL или пустую строку, если сессия умерла."""
    try:
        url: Optional[str] = driver.current_url
        return url or ""
    except Exception:
        return ""


def new_driver() -> webdriver.Chrome:
    options = Options()
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ru")
    return webdriver.Chrome(options=options)


def collect_cookies(
    driver: webdriver.Chrome,
) -> List[Dict[str, Any]]:
    """Собирает куки с доменов кабинета и Skyeng ID."""
    collected: List[Dict[str, Any]] = []
    for url in (CABINET_URL, ID_URL):
        driver.get(url)
        time.sleep(3)
        cookies = driver.get_cookies()
        print(f"Домен {url}: куки {[c['name'] for c in cookies]}")
        collected.extend(cookies)
    return collected


def main() -> None:
    driver: webdriver.Chrome = new_driver()
    driver.get(LOGIN_URL)
    print("В открывшемся окне Chrome выполните вход полностью:")
    print("1) введите почту, при необходимости галочку согласия;")
    print("2) запросите код и введите его из письма;")
    print("3) дождитесь, когда в адресной строке будет teachers.skyeng.ru")
    print(f"Скрипт ждёт до {WAIT_SECONDS} секунд.")
    deadline: float = time.time() + WAIT_SECONDS
    logged_in: bool = False
    while time.time() < deadline:
        url: str = safe_current_url(driver)
        if not url:
            print("Сессия браузера оборвалась — перезапускаю браузер.")
            try:
                driver.quit()
            except Exception:
                pass
            driver = new_driver()
            driver.get(LOGIN_URL)
            time.sleep(5)
            continue
        if "teachers.skyeng.ru" in url and "id.skyeng.ru" not in url:
            logged_in = True
            break
        time.sleep(2)
    if not logged_in:
        print("Кабинет не открылся за отведённое время.")
        print("Проверьте вход (код, согласия) и запустите снова.")
        driver.quit()
        return
    cookies: List[Dict[str, Any]] = collect_cookies(driver)
    names: list = [c["name"] for c in cookies]
    print("URL:", safe_current_url(driver))
    print("Cookies:", names)
    if "token_global" not in names:
        print("token_global не найден. Пройдите вход заново.")
        driver.quit()
        return
    with open(COOKIES_FILE, "w", encoding="utf-8") as file:
        json.dump(cookies, file, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(cookies)} кук в {COOKIES_FILE}")
    driver.quit()


if __name__ == "__main__":
    main()
