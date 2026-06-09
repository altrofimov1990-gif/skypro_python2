from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_session_storage_auth():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд

    try:
        # Шаг 1: Откройте страницу https://gitflic.ru/
        driver.get("https://gitflic.ru/")

        # Шаг 2: Установите cookie пользователя 1 (замените на реальные cookie)
        user1_cookies = [
            {'name': 'cookie_name_1', 'value': 'cookie_value_1', 'domain': 'gitflic.ru'},
            {'name': 'cookie_name_2', 'value': 'cookie_value_2', 'domain': 'gitflic.ru'}
        ]
        for cookie in user1_cookies:
            driver.add_cookie(cookie)

        # Шаг 3: Обновите страницу
        driver.refresh()

        # Ждём загрузки страницы после обновления
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Шаг 4: Перейдите на страницу пользователя 1
        # Предполагаем, что после авторизации есть кнопка/ссылка «Профиль»
        profile_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Профиль') or contains(@href, '/profile')]"))
        )
        profile_link.click()

        # Шаг 5: Сохраните текущий URL для пользователя 1
        user1_url = driver.current_url
        print(f"URL пользователя 1: {user1_url}")

        # Шаг 6: Разлогиньтесь (очистите куки)
        driver.delete_all_cookies()

        # Обновите страницу после очистки куки
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Шаг 7: Установите cookie пользователя 2 (замените на реальные cookie)
        user2_cookies = [
            {'name': 'cookie_name_1', 'value': 'cookie_value_1_user2', 'domain': 'gitflic.ru'},
            {'name': 'cookie_name_2', 'value': 'cookie_value_2_user2', 'domain': 'gitflic.ru'}
        ]
        for cookie in user2_cookies:
            driver.add_cookie(cookie)

        # Шаг 8: Обновите страницу
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Шаг 9: Перейдите на страницу пользователя 2
        profile_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Профиль') or contains(@href, '/profile')]"))
        )
        profile_link.click()

        # Шаг 10: Сохраните текущий URL для пользователя 2
        user2_url = driver.current_url
        print(f"URL пользователя 2: {user2_url}")

        # Шаг 11: Проверьте, что URL для пользователя 1 и пользователя 2 различаются
        assert user1_url != user2_url, (
            f"URL пользователей совпадают!\n"
            f"Пользователь 1: {user1_url}\n"
            f"Пользователь 2: {user2_url}"
        )
        print("Проверка пройдена: URL для разных пользователей различаются.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        # Закрываем браузер в любом случае
        driver.quit()

# Запуск теста
if __name__ == "__main__":
    test_session_storage_auth()