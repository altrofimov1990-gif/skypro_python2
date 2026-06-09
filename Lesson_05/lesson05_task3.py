from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def input_field_test():
    # Инициализация драйвера Firefox
    driver = webdriver.Firefox()

    try:
        # Открытие страницы
        driver.get("http://the-internet.herokuapp.com/inputs")

        # Ожидание загрузки страницы
        time.sleep(2)

        # Явное ожидание появления поля ввода и его кликабельности
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        )

        # Ввод текста 12345
        input_field.send_keys("12345")
        print("Введён текст: 12345")

        # Очистка поля
        input_field.clear()
        print("Поле очищено")

        # Ввод текста 54321
        input_field.send_keys("54321")
        print("Введён текст: 54321")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие браузера
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    input_field_test()