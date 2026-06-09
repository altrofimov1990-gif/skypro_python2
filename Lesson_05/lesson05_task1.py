from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def click_blue_button():
    # Инициализация драйвера Chrome (без указания пути к ChromeDriver)
    driver = webdriver.Chrome()

    try:
        # Открытие страницы
        driver.get("http://uitestingplayground.com/classattr")

        # Ожидание загрузки страницы (2 секунды)
        time.sleep(2)

        # Поиск кнопки по CSS‑классу и клик по ней
        button = driver.find_element(By.CSS_SELECTOR, '.btn-primary')
        button.click()

        print("Кнопка успешно нажата!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие браузера
        driver.quit()

if __name__ == "__main__":
    click_blue_button()