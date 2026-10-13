import pytest
import allure
from pathlib import Path

# ВАЖНО: полный импорт, потому что мы запускаем pytest из корня проекта
from lesson_10.login_page import LoginPage


@allure.title("Диагностика: открытие страницы логина Swag Labs")
def test_debug_open_login_page(driver):
    driver.get("https://www.saucedemo.com/")

    screenshot_path = Path.cwd() / "debug_login_screen.png"
    driver.save_screenshot(str(screenshot_path))
    print(f"Скриншот сохранён: {screenshot_path}")

    print("Current URL:", driver.current_url)
    print("Page Title:", driver.title)

    login = LoginPage(driver)
    try:
        field = login.wait.until(
            lambda d: d.find_element(*login.username_field)
        )
        print("✅ Поле username найдено! Всё ок.")
    except Exception as e:
        print(f"❌ Не удалось найти поле username: {e}")
        raise