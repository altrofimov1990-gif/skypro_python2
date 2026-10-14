"""Диагностика: какие поля и кнопки есть на форме входа id.skyeng.ru."""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://id.skyeng.ru/login")
    time.sleep(8)  # дать SPA полностью отрисоваться

    print("URL:", driver.current_url)
    print("--- IFRAMES ---")
    for f in driver.find_elements("css selector", "iframe"):
        print("IFRAME:", f.get_attribute("src"))
    print("--- INPUTS ---")
    for i in driver.find_elements("css selector", "input"):
        print(
            "INPUT name=", repr(i.get_attribute("name")),
            "| type=", repr(i.get_attribute("type")),
            "| placeholder=", repr(i.get_attribute("placeholder")),
            "| id=", repr(i.get_attribute("id")),
            "| class=", repr(i.get_attribute("class")),
        )
    print("--- BUTTONS ---")
    for b in driver.find_elements("css selector", "button"):
        print(
            "BUTTON text=", repr(b.text),
            "| type=", repr(b.get_attribute("type")),
            "| class=", repr(b.get_attribute("class")),
        )
finally:
    input("Нажмите Enter, чтобы закрыть браузер...")
    driver.quit()