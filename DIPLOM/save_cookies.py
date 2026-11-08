# save_cookies.py
"""Снимает сессию: логин руками в открывшемся окне, затем сохранение куки."""
import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--lang=ru")
driver = webdriver.Chrome(options=options)
driver.get("https://id.skyeng.ru/login")

print("Логиньтесь в открывшемся окне.")
print("Когда кабинет откроется, вернитесь в консоль.")

for i in range(180, 0, -1):
    print(f"  осталось {i} сек.   ", end="\r")
    time.sleep(1)
    if "teachers.skyeng.ru" in driver.current_url:
        print("\nКабинет открыт — жду 5 секунд для догона куки.")
        time.exit = None  # НЕ ИСПОЛЬЗУЙТЕ ЭТУ СТРОКУ
        break

time.sleep(5)
driver.get("https://teachers.skyeng.ru")
time.sleep(5)

cookies = driver.get_cookies()
out = Path(__file__).parent / "cookies.json"
out.write_text(
    json.dumps(cookies, ensure_ascii=False, indent=2), "utf-8"
)
print(f"Сохранено {len(cookies)} куки в {out}")
input("Нажмите Enter, чтобы закрыть браузер…")
driver.quit()
